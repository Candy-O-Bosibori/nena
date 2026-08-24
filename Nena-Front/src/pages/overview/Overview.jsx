import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import { Disclosure, Listbox } from "@headlessui/react";
import { ChevronUpIcon, ChevronUpDownIcon, CheckIcon } from "@heroicons/react/20/solid";
import SpinReveal from "../../Components/SpinReveal/SpinReveal";
import Button from "../../Components/ui/Button";
import ThemeToggle from "../../Components/ui/ThemeToggle";

const PLACEHOLDER_TOPICS = [
  "Spinning the wheel…",
  "Picking a prompt…",
  "Something worth saying…",
  "Warming up…",
  "Almost there…",
];

const DIFFICULTIES = ["random", "easy", "medium", "hard"];

const MODE_HEADLINE = {
  "random-topic": "Wildcard",
  "interview-prep": "Interview Ready",
  "learn-vocab": "Word Boost",
  "read-aloud": "Practice Reading Aloud",
  "daily-reflection": "Today's Reflection",
};

// No fill, just colored text: pastel traffic-light hues, one deliberate
// exception to the brand's amber/navy-only palette so difficulty reads at a
// glance. Shades chosen to clear 4.5:1 on both the light cream and dark
// near-black page backgrounds (checked: green #4CA96A / #7ED9A0, yellow
// #B08900 / #E8D06A, red #E05F5F / #FF9B9B).
const DIFFICULTY_TONE = {
  easy: "text-[#4CA96A] dark:text-[#7ED9A0]",
  medium: "text-[#B08900] dark:text-[#E8D06A]",
  hard: "text-[#E05F5F] dark:text-[#FF9B9B]",
};

export const Overview = () => {
  const navigate = useNavigate();

  // Core data state
  const [modes, setMode] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nextPractice, setNextPractice] = useState(null);

  // Spin/filter state
  const [activeModeSlug, setActiveModeSlug] = useState(null);
  const [difficulty, setDifficulty] = useState("random");
  const [spinNonce, setSpinNonce] = useState(0);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [frameworks, setFrameworks] = useState([]);
  const [selectedFramework, setSelectedFramework] = useState(null);

  // Initialize active mode once modes load. Always defaults to Random Topic
  // (or the first mode if that slug is ever missing) -- the "pick up where
  // you left off" card can recommend a different mode's topic, but that's a
  // suggestion to click into, not something that should hijack which tab is
  // selected on load.
  useEffect(() => {
    if (modes.length > 0 && !activeModeSlug) {
      const randomTopicMode = modes.find((m) => m.slug === "random-topic");
      setActiveModeSlug(randomTopicMode?.slug || modes[0]?.slug);
    }
  }, [modes, activeModeSlug]);

  const activeMode = modes.find((m) => m.slug === activeModeSlug);
  const accent = activeMode?.accent_color || "#DC9750";

  // Main data fetch. Runs regardless of auth state -- modes/topics are public,
  // and next-practice/frameworks degrade gracefully via the .catch() fallbacks
  // below when there's no token.
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [modesRes, nextPracticeRes, frameworksRes] = await Promise.all([
          api.get("/modes"),
          api.get("/next-practice").catch(() => ({ data: null })),
          api.get("/frameworks").catch(() => ({ data: { frameworks: [] } })),
        ]);

        setMode(modesRes.data);
        setNextPractice(nextPracticeRes.data);
        setFrameworks(frameworksRes.data.frameworks || []);
      } catch (error) {
        console.error("Error fetching overview data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Spin reveal: resolve function that fetches the topic
  const resolveTopic = async () => {
    if (!activeMode) throw new Error("No active mode");

    const isShingled = activeModeSlug === "daily-reflection";
    const url = isShingled
      ? "/topics/today?mode=daily-reflection"
      : `/topics/random?mode=${activeModeSlug}${
          difficulty !== "random" ? `&difficulty=${difficulty}` : ""
        }`;

    const response = await api.get(url);
    return response.data;
  };

  const handleTopicSettled = (topic) => {
    setSelectedTopic(topic);
    if (topic?.meta?.suggested_framework) {
      setSelectedFramework(topic.meta.suggested_framework);
    }
  };

  const handleTopicError = (err) => {
    console.error("Failed to load topic:", err);
  };

  const goToPractice = (topic, mode, framework) => {
    navigate(`/practice/${mode?.slug}`, {
      state: { topic, mode, selectedFramework: framework ?? null },
    });
  };

  // Render topic card based on mode type
  const renderTopicCard = (topic, isSettled) => {
    if (!topic) return null;

    const isLearnVocab = activeModeSlug === "learn-vocabulary";
    const isReadAloud = activeModeSlug === "read-aloud";
    const reveal = isSettled ? "animate-fade-up" : "opacity-0";

    if (isLearnVocab) {
      return (
        <div className={`text-center ${reveal}`}>
          <p className="font-display text-3xl font-normal tracking-tight text-ink md:text-4xl">
            {topic.text}
          </p>
          {topic.meta?.part_of_speech && (
            <p className="mt-2 text-xs uppercase tracking-[0.18em] text-ink-muted">
              {topic.meta.part_of_speech}
            </p>
          )}
          {topic.meta?.definition && (
            <p className="mt-4 text-base leading-relaxed text-ink-soft">
              {topic.meta.definition}
            </p>
          )}
          {topic.meta?.example_sentence && (
            <p className="mt-3 text-sm italic text-ink-muted">
              “{topic.meta.example_sentence}”
            </p>
          )}
        </div>
      );
    }

    if (isReadAloud) {
      return (
        <div className={`text-center ${reveal}`}>
          <p className="font-serif-reading text-xl leading-relaxed text-ink md:text-2xl">
            {topic.text}
          </p>
          <p className="mt-4 text-xs uppercase tracking-[0.18em] text-ink-muted">
            Target {topic.meta?.target_seconds || 60}s · {topic.meta?.word_count || 0} words
          </p>
        </div>
      );
    }

    return (
      <div className={`text-center ${reveal}`}>
        <p className="font-display text-2xl font-normal leading-snug tracking-tight text-ink md:text-[2.1rem]">
          {topic.text}
        </p>
        {topic.difficulty && (
          <span
            className={`mt-5 inline-block text-[11px] font-bold uppercase tracking-[0.14em] ${
              DIFFICULTY_TONE[topic.difficulty] || "text-ink-soft"
            }`}
          >
            {topic.difficulty}
          </span>
        )}
      </div>
    );
  };

  const isDaily = activeModeSlug === "daily-reflection";
  const isSpinDisabledForDaily = isDaily && selectedTopic !== null;

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-cream">
        <div className="flex flex-col items-center gap-4">
          <span className="h-9 w-9 animate-spin rounded-full border-[3px] border-line border-t-primary" />
          <p className="text-sm text-ink-muted">Loading your practice…</p>
        </div>
      </div>
    );
  }

  const isSignedIn = Boolean(localStorage.getItem("access_token"));

  return (
    <div className="min-h-screen bg-cream">
      {!isSignedIn && (
        <div className="flex items-center justify-end gap-3 px-5 pt-6">
          <ThemeToggle />
          <Button onClick={() => navigate("/signin")} size="sm">
            Sign in
          </Button>
        </div>
      )}
      <div className="mx-auto flex w-full max-w-3xl  flex-col items-center px-5 pb-24 pt-8 md:pt-12">
        {/* ---------- Continue where you left off ---------- */}
        {nextPractice?.topic && (
          <button
            onClick={() =>
              goToPractice(
                nextPractice.topic,
                nextPractice.mode,
                nextPractice.topic?.meta?.suggested_framework
              )
            }
            className="mt-8 w-full mb-10 rounded-2xl border border-line bg-surface p-4 text-left transition-all duration-200 hover:border-primary/40 hover:shadow-sm focus-ring"
          >
            <p className="text-[15px] font-bold uppercase tracking-[0.16em] text-primary-700">
              Pick up where you left off
            </p>
            <p className="mt-1.5 line-clamp-2 text-sm font-semibold text-ink">
              {nextPractice.topic.text}
            </p>
            {nextPractice.reason && (
              <p className="mt-1 text-xs text-ink-muted">{nextPractice.reason}</p>
            )}
          </button>
        )}
        
        {/* ---------- Mode tabs ---------- */}
        <nav className="w-full">
          <div className="no-scrollbar flex gap-2 overflow-x-auto rounded-lg border border-line bg-surface/70 p-1.5 backdrop-blur">
            {modes.map((mode) => {
              const active = mode.slug === activeModeSlug;
              return (
                <button
                  key={mode.slug}
                  onClick={() => {
                    setActiveModeSlug(mode.slug);
                    setSelectedTopic(null);
                    setSelectedFramework(null);
                  }}
                  style={active ? { backgroundColor: mode.accent_color } : undefined}
                  className={[
                    "flex-1 whitespace-nowrap rounded-lg px-4 py-2.5 text-sm font-semibold",
                    "transition-all duration-200 focus-ring",
                    active
                      // Forest ink, not white: mode accent_color values sit on
                      // the gold/orange scales, which stay light even at their
                      // darkest shades -- white text fails contrast there.
                      ? "text-ink shadow-sm"
                      : "text-ink-soft hover:bg-primary-soft/60 hover:text-ink",
                  ].join(" ")}
                >
                  {mode.name}
                </button>
              );
            })}
          </div>
        </nav>

        {/* ---------- Mode explainer ---------- */}
        <header className="mt-10 text-center md:mt-14">
          <h1 className="font-display text-4xl font-normal tracking-tight text-ink md:text-5xl">
            {MODE_HEADLINE[activeModeSlug] || activeMode?.name || "Practice"}
          </h1>
          <p className="mt-3 text-base text-ink-soft">
            {activeMode?.explainer || activeMode?.description || "Pick a prompt and start speaking."}
          </p>
        </header>

        {/* ---------- Steps ---------- */}
        <ol className="mt-8 flex flex-wrap items-center justify-center gap-x-3 gap-y-2 text-sm font-semibold text-ink-soft">
          {!isDaily && (
            <li className="flex items-center gap-2">
              <span>
                <span className="text-primary-700">1)</span> Pick a difficulty
              </span>
              <Listbox
                value={difficulty}
                onChange={(level) => {
                  setDifficulty(level);
                  setSelectedTopic(null);
                }}
              >
                <div className="relative">
                  <Listbox.Button className="flex items-center gap-1.5 rounded-lg border border-line bg-surface px-3 py-1.5 text-sm font-semibold capitalize text-ink transition-colors hover:border-ink-muted focus-ring">
                    <span>{difficulty}</span>
                    <ChevronUpDownIcon className="h-4 w-4 shrink-0 text-ink-muted" />
                  </Listbox.Button>
                  <Listbox.Options className="absolute z-10 mt-1 w-36 overflow-hidden rounded-lg border border-line bg-surface shadow-lg focus:outline-none">
                    {DIFFICULTIES.map((level) => (
                      <Listbox.Option
                        key={level}
                        value={level}
                        className="flex cursor-pointer items-center justify-between gap-2 px-4 py-2.5 text-sm font-semibold capitalize text-ink data-[focus]:bg-cream"
                      >
                        {({ selected }) => (
                          <>
                            <span>{level}</span>
                            {selected && <CheckIcon className="h-4 w-4 shrink-0 text-ink-muted" />}
                          </>
                        )}
                      </Listbox.Option>
                    ))}
                  </Listbox.Options>
                </div>
              </Listbox>
            </li>
          )}
          {["Get a topic", "Set your timer", "Record & speak"].map((step, i) => (
            <li key={step} className="flex items-center gap-3">
              {(i > 0 || !isDaily) && <span className="text-line">·</span>}
              <span>
                <span className="text-primary-700">{isDaily ? i + 1 : i + 2})</span> {step}
              </span>
            </li>
          ))}
        </ol>

        {/* ---------- Spin reveal stage ---------- */}
        <section className="mt-8 w-full">
          <SpinReveal
            candidates={PLACEHOLDER_TOPICS}
            resolve={resolveTopic}
            spinKey={activeModeSlug ? `${activeModeSlug}-${difficulty}-${spinNonce}` : ""}
            onSettle={handleTopicSettled}
            onError={handleTopicError}
            renderResult={renderTopicCard}
            accent={accent}
          />
        </section>

        {/* ---------- Primary actions ---------- */}
        <div className="mt-8 flex w-full flex-col items-center gap-3 sm:flex-row sm:justify-center">
          <Button
            size="lg"
            onClick={() => setSpinNonce((n) => n + 1)}
            disabled={isSpinDisabledForDaily}
            className="w-full sm:w-auto sm:min-w-[168px]"
            style={{ backgroundColor: accent }}
          >
            Generate!
          </Button>
          <Button
            size="lg"
            variant="secondary"
            onClick={() => goToPractice(selectedTopic, activeMode, selectedFramework)}
            disabled={!selectedTopic}
            className="w-full sm:w-auto sm:min-w-[168px]"
          >
            Timer →
          </Button>
        </div>

        {isDaily && selectedTopic && (
          <p className="mt-4 text-center text-xs text-ink-muted">
            Today’s reflection is fixed — come back tomorrow for a new one.
          </p>
        )}

        {/* ---------- Frameworks ---------- */}
        {selectedTopic && frameworks.length > 0 && (
          <section className="mt-12 w-full">
            <h2 className="mb-1 text-center text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">
              Optional structure
            </h2>
            <p className="mb-3 text-center text-xs text-ink-muted">
              A framework is a simple shape for your answer, made of a few short beats to hit in order. Pick one if you want a bit of scaffolding, or skip it and speak freely.
            </p>
            <div className="divide-y divide-line overflow-hidden rounded-2xl bg-surface">
              {frameworks.map((fw) => (
                <Disclosure key={fw.slug}>
                  {({ open }) => (
                    <div>
                      <Disclosure.Button className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left transition-colors hover:bg-cream focus-ring">
                        <span className="flex items-center gap-3">
                          <input
                            type="radio"
                            checked={selectedFramework === fw.slug}
                            onChange={(e) => {
                              e.stopPropagation();
                              setSelectedFramework(fw.slug);
                            }}
                            onClick={(e) => e.stopPropagation()}
                            className="accent-primary"
                          />
                          <span className="flex flex-col">
                            <span className="text-sm font-semibold text-ink">{fw.name}</span>
                            {fw.best_for && (
                              <span className="text-xs text-ink-muted">{fw.best_for}</span>
                            )}
                          </span>
                        </span>
                        <ChevronUpIcon
                          className={`h-4 w-4 shrink-0 text-ink-muted transition-transform duration-200 ${
                            open ? "" : "rotate-180"
                          }`}
                        />
                      </Disclosure.Button>
                      <Disclosure.Panel className="px-5 pb-4 text-sm text-ink-soft">
                        {Array.isArray(fw.steps) && fw.steps.length > 0 && (
                          <ul className="space-y-2">
                            {fw.steps.map((step, idx) => (
                              <li key={idx} className="flex gap-2">
                                <span className="font-bold text-primary-700">
                                  {(typeof step === "object" && step?.letter) || idx + 1}.
                                </span>
                                <span>
                                  {typeof step === "string" ? (
                                    step
                                  ) : (
                                    <>
                                      {step?.label && (
                                        <span className="font-semibold text-ink">{step.label}: </span>
                                      )}
                                      {step?.description || ""}
                                    </>
                                  )}
                                </span>
                              </li>
                            ))}
                          </ul>
                        )}
                      </Disclosure.Panel>
                    </div>
                  )}
                </Disclosure>
              ))}
            </div>
            {selectedFramework && (
              <button
                onClick={() => setSelectedFramework(null)}
                className="mx-auto mt-3 block text-xs font-semibold text-ink-muted hover:text-primary-700 focus-ring"
              >
                Clear selection
              </button>
            )}
          </section>
        )}
      </div>
    </div>
  );
};

export default Overview;
