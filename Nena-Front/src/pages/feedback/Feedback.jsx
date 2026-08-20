import React from 'react'
import { useState, useEffect } from "react";
import { Dialog } from "@headlessui/react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from 'jwt-decode';
import api from "../../api/api";

export const Feedback = () => {
  const [recordings, setRecordings] = useState([]);
  const [selectedRecording, setSelectedRecording] = useState(null);
  const [trends, setTrends] = useState(null);
  const [trendsLoading, setTrendsLoading] = useState(false);
  const [nextPractice, setNextPractice] = useState(null);
  const [nextPracticeLoading, setNextPracticeLoading] = useState(false);
  const navigate = useNavigate();

 useEffect(() => {
    const token = localStorage.getItem('token');
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
  const token = localStorage.getItem("token");
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


  // Mode colors
  const modeColors = {
    "Explain a Concept": "bg-[#F25019] text-white shadow-lg shadow-[#F25019]/40",
    "Read Aloud": "bg-[#BBC53B] text-white hadow-lg shadow-[#BBC53B]/40",
    "Tell A Story": "bg-[#EEB300] text-white shadow-lg shadow-[#FFC107]/40",
    "Random Word": "bg-[#CC3C0C]/80 text-white shadow-lg shadow-[#CC3C0C]/40",
  };

  return (
    <div className="flex-1 p-7 bg-[#fffaf7] overflow-y-auto">
      <h1 className="text-xl bg-[#FFEEE3] -m-7 p-6 text-[#F25019] font-semibold mb-6">Feed Back</h1>

      {/* Empty State */}
      {recordings.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <p className="text-lg text-gray-600 mb-4">
            You have no videos yet, therefore we can’t give feedback.
          </p>
          <button
            onClick={() => navigate("/overview")}
            className="px-6 py-2 bg-orange-500 text-white rounded-lg shadow-md hover:bg-orange-600"
          >
            Go to Overview
          </button>
        </div>
      ) : (
        Object.entries(recordingsByDate).map(([date, recs]) => (
          <div key={date} className="mb-5">
            <h2 className="text-lg font-semibold ">{date}</h2>
            {/* Horizontal scroll for video cards */}
            <div className="flex gap-4 overflow-x-auto pb-2">
              {recs.map((rec) => (
                <div
                  key={rec.id}
                  className={`md:max-w-[500px] min-h-[150px] max-w-full p-4 md:p-6 rounded-2xl shadow-md cursor-pointer flex-shrink-0 ${modeColors[rec.mode.name] || "bg-gray-300"}`}
                  onClick={() => setSelectedRecording(rec)}
                >
                  <h3 className="font-semibold text-lg">{rec.mode.name}</h3>
                  <p className="text-sm opacity-90">{rec.mode.description}</p>
                </div>
              ))}
            </div>
          </div>
        ))
      )}

      {/* Modal */}
      <Dialog
        open={!!selectedRecording}
        onClose={() => setSelectedRecording(null)}
        className="relative z-50"
      >
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center ">
          <Dialog.Panel className="bg-white rounded-xl  w-full max-w-3xl shadow-lg">
            {selectedRecording && (
              <>
              <div className='flex h-[70vh]'>
                <div className='py-6  overflow-auto pl-6 flex-1 min-w-[400px] md:w-4/6'>
                <div className="flex  justify-between items-center mb-4">
                  <h2 className="text-xl  font-semibold">
                    {selectedRecording.mode.name}.
                    <span className="ml-2 text-gray-500 text-sm">
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
                <div className="bg-[#FFEEE3]/40 p-4 rounded-lg text-sm leading-relaxed mb-4">
                  <h3 className="font-semibold mb-2">Transcription</h3>
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
                        if (isFiller) highlightClass = "bg-red-100 px-1 rounded";
                        else if (isVocab) highlightClass = "bg-green-100 px-1 rounded";
                        else if (isHedge) highlightClass = "bg-amber-100 px-1 rounded"; // (9e)

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
               
                <div className='md:w-2/6 flex flex-col justify-between  rounded-lg ml-5 p-6  bg-[#FFEEE3] overflow-y-auto'>
                {/* Feedback Stats (9e) */}
                <div className="flex flex-col  gap-4 text-sm">
                  {/* Pace */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Pace</span>
                      <span className="text-xs text-gray-600">
                        {trends?.summary?.pace_wpm_avg ? `Avg: ${Math.round(trends.summary.pace_wpm_avg)}` : ''}
                      </span>
                    </div>
                    <p>{Math.round(selectedRecording.feedback?.pace_wpm || 0)} words/min</p>
                  </div>

                  {/* Filler Words */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Filler Words</span>
                      <span className="text-xs text-gray-600">
                        {trends?.summary?.filler_words_avg ? `Avg: ${trends.summary.filler_words_avg.toFixed(1)}` : ''}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.filler_words}</p>
                  </div>

                  {/* Hedges (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Hedges</span>
                      <span className="text-xs text-gray-600">
                        {trends?.summary?.hedge_count_avg ? `Avg: ${trends.summary.hedge_count_avg.toFixed(1)}` : ''}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.hedge_count || 0}</p>
                  </div>

                  {/* Time to Point (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Time to Point</span>
                      <span className="text-xs text-gray-600">
                        {trends?.summary?.time_to_point_seconds_avg ? `Avg: ${trends.summary.time_to_point_seconds_avg.toFixed(1)}s` : ''}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.time_to_point_seconds ? `${selectedRecording.feedback.time_to_point_seconds.toFixed(1)}s` : 'N/A'}</p>
                  </div>

                  {/* Concreteness (9e) */}
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Concreteness</span>
                      <span className="text-xs text-gray-600">
                        {trends?.summary?.concreteness_ratio_avg ? `Avg: ${(trends.summary.concreteness_ratio_avg * 100).toFixed(0)}%` : ''}
                      </span>
                    </div>
                    <p>{selectedRecording.feedback?.concreteness_ratio ? `${(selectedRecording.feedback.concreteness_ratio * 100).toFixed(0)}%` : 'N/A'}</p>
                  </div>

                  {/* Vocabulary */}
                  <div>
                    <span className="font-semibold">Vocabulary</span>
                    {selectedRecording.feedback?.vocabulary_list?.length === 0 ? (
                      <span className="text-gray-600">No new words</span>
                    ) : (
                      <div className="flex flex-wrap gap-2 mt-1">
                        {selectedRecording.feedback.vocabulary_list.map((word, idx) => (
                          <span
                            key={idx}
                            className=" text-green-800 px-2 py-1 rounded-full text-sm bg-green-100"
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
                      <p className="font-semibold mb-2 text-[#F25019]">💡 Coaching</p>
                      <p className="text-xs text-gray-700 mb-2">{selectedRecording.feedback.coach_notes}</p>
                      {selectedRecording.feedback?.strongest_moment && (
                        <p className="text-xs italic text-gray-600 border-l-2 border-[#F25019] pl-2 mb-2">
                          "{selectedRecording.feedback.strongest_moment}"
                        </p>
                      )}

                      {/* Framework Adherence Chips (9f) */}
                      {selectedRecording.feedback?.framework_adherence && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {selectedRecording.feedback.framework_adherence.map((step) => (
                            <span
                              key={step}
                              className={`text-xs px-2 py-1 rounded-full ${
                                step.followed
                                  ? "bg-[#F25019] text-white"
                                  : "border border-gray-300 text-gray-600"
                              }`}
                            >
                              {step.letter}
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
                    <p className="font-semibold mb-2 text-[#F25019]">👉 Continue Practice</p>
                    <div className="bg-gray-50 rounded p-2 mb-2">
                      <p className="text-xs font-medium text-gray-800 mb-1">{nextPractice.topic?.text}</p>
                      <p className="text-xs text-gray-600">{nextPractice.reason}</p>
                    </div>
                    <button
                      onClick={() => navigate(`/practice/${nextPractice.mode?.slug}`)}
                      className="w-full px-3 py-1 bg-[#F25019] text-white rounded text-xs hover:bg-[#CC3C0C] font-medium"
                    >
                      Start Practice
                    </button>
                  </div>
                )}

                <div className="mt-6 text-right">
                  <div className="flex justify-end gap-3">
                    <button
                      onClick={() => setSelectedRecording(null)}
                      className="px-6 py-2 bg-gray-400 text-white rounded-lg shadow-md hover:bg-gray-500"
                    >
                      Close
                    </button>
                    <button
                      onClick={() => handleDeleteRecording(selectedRecording.id)}
                      className="px-6 py-2 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600"
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
