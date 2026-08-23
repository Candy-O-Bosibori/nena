import React from 'react'
import { useState, useEffect } from "react";
import { Dialog } from "@headlessui/react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from 'jwt-decode';
import api from "../../api/api";
import { fmt, fmtInt, fmtPercent } from "../../utils/format";
import Button from "../../Components/ui/Button";

// coach_notes arrives as {opening, clarity, evidence, conclusion}. List the known
// keys so they render in a sensible order, then append any others the model adds
// rather than silently dropping them.
const COACH_NOTE_ORDER = ["opening", "clarity", "evidence", "conclusion"];

const orderedCoachNotes = (notes) => {
  if (!notes || typeof notes !== "object") return [];
  const known = COACH_NOTE_ORDER.filter((k) => notes[k]);
  const extra = Object.keys(notes).filter(
    (k) => !COACH_NOTE_ORDER.includes(k) && notes[k]
  );
  return [...known, ...extra];
};

// framework_adherence arrives as {step_1: "weak"|"medium"|"strong", ...}.
const ADHERENCE_STYLES = {
  strong: "bg-primary text-on-primary",
  medium: "bg-primary-200 text-primary-700",
  weak: "border border-line text-ink-muted",
};

const frameworkSteps = (adherence) => {
  if (!adherence || typeof adherence !== "object") return [];
  if (Array.isArray(adherence)) return [];
  return Object.entries(adherence).filter(([, rating]) => rating);
};

export const Feedback = () => {
  const [recordings, setRecordings] = useState([]);
  const [selectedRecording, setSelectedRecording] = useState(null);
  const [trends, setTrends] = useState(null);
  const [trendsLoading, setTrendsLoading] = useState(false);
  const [nextPractice, setNextPractice] = useState(null);
  const [nextPracticeLoading, setNextPracticeLoading] = useState(false);
  const navigate = useNavigate();

 useEffect(() => {
    const token = localStorage.getItem('access_token');
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    // Fetch recordings
    fetch('http://127.0.0.1:5000/recordings', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => response.json())
      .then(data => {
        setRecordings(data);
      })
      .catch(error => console.error('Error:', error));

    // Fetch 30-day trends (9e)
    const fetchTrends = async () => {
      setTrendsLoading(true);
      try {
        const response = await api.get('/trends');
        setTrends(response.data);
      } catch (err) {
        console.error('Failed to load trends:', err);
      } finally {
        setTrendsLoading(false);
      }
    };

    // Fetch next practice recommendation (9g)
    const fetchNextPractice = async () => {
      setNextPracticeLoading(true);
      try {
        const response = await api.get('/next-practice');
        setNextPractice(response.data);
      } catch (err) {
        console.error('Failed to load next practice:', err);
      } finally {
        setNextPracticeLoading(false);
      }
    };

    fetchTrends();
    fetchNextPractice();
    }, []);

    const handleDeleteRecording = async (id) => {
  const token = localStorage.getItem("access_token");
  try {
    const response = await fetch(`http://127.0.0.1:5000/recordingById/${id}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (response.ok) {
      // Remove the deleted recording from state
      setRecordings((prev) => prev.filter((rec) => rec.id !== id));
      setSelectedRecording(null); // Close modal
    } else {
      const data = await response.json();
      alert(data.error || "Failed to delete recording");
    }
  } catch (error) {
    console.error("Delete error:", error);
  }
};

  // Group by date
const recordingsByDate = recordings
  .slice()
  .sort((a, b) => new Date(b.created_at) - new Date(a.created_at)) // newest first
  .reduce((acc, rec) => {
    const date = new Date(rec.created_at).toLocaleDateString("en-US", {
      weekday: "long",
      day: "numeric",
      month: "short",
    });
    if (!acc[date]) acc[date] = [];
    acc[date].push(rec);
    return acc;
  }, {});


  return (
    <div className="min-h-screen flex-1 overflow-y-auto bg-cream">
      <div className="mx-auto w-full max-w-4xl px-5 py-10">
        <header className="mb-8">
          <h1 className="font-display text-3xl font-normal tracking-tight text-ink md:text-4xl">
            Your feedback
          </h1>
          <p className="mt-2 text-sm text-ink-soft">
            Every session you’ve recorded, with delivery notes and coaching.
          </p>
        </header>

      {/* Empty State */}
      {recordings.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-3xl border border-dashed border-line bg-surface/60 py-20 text-center">
          <p className="mb-1 text-base font-semibold text-ink">No sessions yet</p>
          <p className="mb-6 max-w-xs text-sm text-ink-soft">
            Record your first practice and your feedback will show up here.
          </p>
          <Button onClick={() => navigate("/overview")}>Start practising</Button>
        </div>
      ) : (
        Object.entries(recordingsByDate).map(([date, recs]) => (
          <div key={date} className="mb-9">
            <h2 className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">
              {date}
            </h2>
            <div className="scroll-slim flex gap-4 overflow-x-auto pb-2">
              {recs.map((rec) => {
                const tint = rec.mode?.accent_color || "#DC9750";
                const hasFeedback = Boolean(rec.feedback);
                return (
                  <button
                    key={rec.id}
                    onClick={() => setSelectedRecording(rec)}
                    className="group w-[280px] shrink-0 rounded-2xl border border-line bg-surface p-5 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-transparent hover:shadow-lg focus-ring"
                  >
                    <span
                      className="mb-3 block h-1.5 w-10 rounded-full"
                      style={{ backgroundColor: tint }}
                    />
                    <h3 className="text-base font-bold text-ink">
                      {rec.mode?.name || "Practice"}
                    </h3>
                    <p className="mt-1 line-clamp-2 text-sm text-ink-soft">
                      {rec.transcription || rec.mode?.description || "No transcript"}
                    </p>
                    <div className="mt-4 flex items-center gap-2 text-[11px] font-semibold text-ink-muted">
                      {hasFeedback ? (
                        <>
                          <span style={{ color: tint }}>
                            {fmtInt(rec.feedback.pace_wpm, "0")} wpm
                          </span>
                          <span className="text-line">|</span>
                          <span>{rec.feedback.filler_words ?? 0} fillers</span>
                        </>
                      ) : (
                        <span>Awaiting analysis</span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ))
      )}

      </div>

      {/* Modal */}
      <Dialog
        open={!!selectedRecording}
        onClose={() => setSelectedRecording(null)}
        className="relative z-50"
      >
        <div className="fixed inset-0 bg-ink/40 backdrop-blur-sm" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center ">
          <Dialog.Panel className="w-full max-w-3xl overflow-hidden rounded-3xl bg-surface shadow-2xl">
            {selectedRecording && (
              <>
              <div className='flex h-[70vh]'>
                <div className='py-6  overflow-auto pl-6 flex-1 min-w-[400px] md:w-4/6'>
                <div className="flex  justify-between items-center mb-4">
                  <h2 className="font-display text-xl font-normal tracking-tight text-ink">
                    {selectedRecording.mode?.name || "Practice"}.
                    <span className="ml-2 text-sm font-medium text-ink-muted">
                      {new Date(selectedRecording.created_at).toLocaleDateString("en-US", {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                      })}
                    </span>
                  </h2>
                </div>
                 {/* Video Player */}
                {selectedRecording.video_url && (
                  <video
                    controls
                    className="w-full rounded-lg mb-4"
                    src={`http://127.0.0.1:5000${selectedRecording.video_url}`}
                  />
                )}

                {/* Transcription */}
                <div className="mb-4 rounded-2xl border border-line bg-cream p-4 text-sm leading-relaxed text-ink-soft">
                  <h3 className="mb-2 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">Transcription</h3>
                  {selectedRecording.transcription ? (
                    <p className="flex flex-wrap gap-1">
                      {selectedRecording.transcription.split(/\s+/).map((word, idx) => {
                        const fillerWords = selectedRecording.feedback?.filler_word_list || [];
                        const vocabWords = selectedRecording.feedback?.vocabulary_list || [];
                        const hedgeWords = selectedRecording.feedback?.hedge_list || [];

                        // Strip trailing punctuation for matching (9e)
                        const cleanWord = word.replace(/[.,!?;:—]$/, '');
                        const lowerClean = cleanWord.toLowerCase();

                        const isFiller = fillerWords.includes(lowerClean);
                        const isVocab = vocabWords.includes(lowerClean);
                        const isHedge = hedgeWords.includes(lowerClean);

                        let highlightClass = "";
                        if (isFiller) highlightClass = "bg-red-100 dark:bg-red-950 dark:text-red-300 px-1 rounded";
                        else if (isVocab) highlightClass = "bg-green-100 dark:bg-green-950 dark:text-green-300 px-1 rounded";
                        else if (isHedge) highlightClass = "bg-amber-100 dark:bg-amber-950 dark:text-amber-300 px-1 rounded"; // (9e)

                        return (
                          <span key={idx} className={highlightClass}>
                            {word}
                          </span>
                        );
                      })}
                    </p>
                  ) : (
                    "No transcription available."
                  )}
                </div>
               </div>
               
                <div className='scroll-slim ml-5 flex w-full flex-col justify-between overflow-y-auto rounded-2xl bg-cream p-6 md:w-2/6'>
                {/* No analysis yet: say so rather than showing a column of zeroes */}
                {!selectedRecording.feedback && (
                  <div className="text-sm text-ink-soft mb-4 pb-4 border-b border-line">
                    <p className="mb-1 font-semibold text-ink">No analysis for this recording</p>
                    <p className="text-xs">Feedback wasn't generated when this was submitted, so the metrics below are empty.</p>
                  </div>
                )}
                {/* Feedback Stats (9e) */}
                <div className="flex flex-col  gap-4 text-sm">
                  {/* Pace */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-ink">Pace</span>
                      <span className="text-xs text-ink-muted">
                        {fmtInt(trends?.summary?.pace_wpm_avg) && `Avg: ${fmtInt(trends?.summary?.pace_wpm_avg)}`}
                      </span>
                    </div>
                    <p>{fmtInt(selectedRecording.feedback?.pace_wpm, "0")} words/min</p>
                  </div>

                  {/* Filler Words */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Filler Words</span>
                      <span className="text-xs text-ink-muted">
                        {fmt(trends?.summary?.filler_words_avg) && `Avg: ${fmt(trends?.summary?.filler_words_avg)}`}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.filler_words ?? 0}</p>
                  </div>

                  {/* Hedges (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Hedges</span>
                      <span className="text-xs text-ink-muted">
                        {fmt(trends?.summary?.hedge_count_avg) && `Avg: ${fmt(trends?.summary?.hedge_count_avg)}`}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.hedge_count || 0}</p>
                  </div>

                  {/* Time to Point (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Time to Point</span>
                      <span className="text-xs text-ink-muted">
                        {fmt(trends?.summary?.time_to_point_seconds_avg) && `Avg: ${fmt(trends?.summary?.time_to_point_seconds_avg)}s`}
                      </span>
                    </div>
                    <p>{fmt(selectedRecording.feedback?.time_to_point_seconds, 1, "N/A")}{fmt(selectedRecording.feedback?.time_to_point_seconds, 1, "") && "s"}</p>
                  </div>

                  {/* Concreteness (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Concreteness</span>
                      <span className="text-xs text-ink-muted">
                        {fmtPercent(trends?.summary?.concreteness_ratio_avg) && `Avg: ${fmtPercent(trends?.summary?.concreteness_ratio_avg)}%`}
                      </span>
                    </div>
                    <p>{fmtPercent(selectedRecording.feedback?.concreteness_ratio, "N/A")}{fmtPercent(selectedRecording.feedback?.concreteness_ratio, "") && "%"}</p>
                  </div>

                  {/* Vocabulary */}
                  <div>
                    <span className="font-semibold">Vocabulary</span>
                    {!selectedRecording.feedback?.vocabulary_list?.length ? (
                      <span className="text-ink-muted">No new words</span>
                    ) : (
                      <div className="flex flex-wrap gap-2 mt-1">
                        {selectedRecording.feedback.vocabulary_list.map((word, idx) => (
                          <span
                            key={idx}
                            className=" text-green-800 dark:text-green-300 px-2 py-1 rounded-full text-sm bg-green-100 dark:bg-green-950"
                          >
                            {word}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Coaching Block (9f) */}
                  {selectedRecording.feedback?.coach_notes && (
                    <div className="border-t pt-3 mt-3">
                      <p className="mb-2 text-[11px] font-bold uppercase tracking-[0.16em] text-primary-700">💡 Coaching</p>
                      {/* coach_notes is a dict of labelled sections
                          ({opening, clarity, evidence, conclusion}), not a string. */}
                      {typeof selectedRecording.feedback.coach_notes === "string" ? (
                        <p className="text-xs text-ink-soft mb-2">
                          {selectedRecording.feedback.coach_notes}
                        </p>
                      ) : (
                        <div className="flex flex-col gap-2 mb-2">
                          {orderedCoachNotes(
                            selectedRecording.feedback.coach_notes
                          ).map((key) => (
                            <div key={key}>
                              <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-ink-muted">
                                {key}
                              </p>
                              <p className="text-xs text-ink-soft">
                                {selectedRecording.feedback.coach_notes[key]}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                      {selectedRecording.feedback?.strongest_moment && (
                        <p className="text-xs italic text-ink-muted border-l-2 border-primary pl-2 mb-2">
                          "{selectedRecording.feedback.strongest_moment}"
                        </p>
                      )}

                      {/* Framework Adherence Chips (9f).
                          Shape is {step_1: "weak"|"medium"|"strong", ...}. */}
                      {frameworkSteps(selectedRecording.feedback?.framework_adherence)
                        .length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {frameworkSteps(
                            selectedRecording.feedback.framework_adherence
                          ).map(([step, rating]) => (
                            <span
                              key={step}
                              title={`${step.replace(/_/g, " ")}: ${rating}`}
                              className={`text-xs px-2 py-1 rounded-full ${
                                ADHERENCE_STYLES[String(rating).toLowerCase()] ||
                                "border border-line text-ink-muted"
                              }`}
                            >
                              {step.replace(/^step_/i, "")} · {rating}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Next Practice CTA (9g) */}
                {nextPractice && (
                  <div className="border-t pt-3 mt-3">
                    <p className="mb-2 text-[11px] font-bold uppercase tracking-[0.16em] text-primary-700">👉 Continue Practice</p>
                    <div className="bg-cream rounded p-2 mb-2">
                      <p className="mb-1 text-xs font-semibold text-ink">{nextPractice.topic?.text}</p>
                      <p className="text-xs text-ink-muted">{nextPractice.reason}</p>
                    </div>
                    <button
                      onClick={() => navigate(`/practice/${nextPractice.mode?.slug}`)}
                      className="w-full px-3 py-1 bg-primary text-on-primary rounded text-xs hover:bg-primary-hover font-medium"
                    >
                      Start Practice
                    </button>
                  </div>
                )}

                <div className="mt-6 text-right">
                  <div className="flex justify-end gap-3">
                    <button
                      onClick={() => setSelectedRecording(null)}
                      className="rounded-xl border border-line bg-surface px-5 py-2.5 text-sm font-semibold text-ink-soft transition-colors hover:text-ink"
                    >
                      Close
                    </button>
                    <button
                      onClick={() => handleDeleteRecording(selectedRecording.id)}
                      className="px-6 py-2 bg-danger text-white rounded-lg shadow-md hover:opacity-90 transition-opacity"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                </div>
              </div>
              </>
            )}
          </Dialog.Panel>
        </div>
        
      </Dialog>
    </div>
  );
}
