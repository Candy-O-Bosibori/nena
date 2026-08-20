import React, { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Disclosure } from "@headlessui/react";
import { ChevronUpIcon } from "@heroicons/react/20/solid";
import api from "../../api/api";

export const Practice = () => {
  const { modeSlug } = useParams();
  const navigate = useNavigate();

  const audioRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);

  const [stream, setStream] = useState(null);
  const [recording, setRecording] = useState(false);
  const [paused, setPaused] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [timer, setTimer] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [recordingId, setRecordingId] = useState(null);
  const [mode, setMode] = useState(null);
  const [loading, setLoading] = useState(true);

  // Topic selection state (9b)
  const [topic, setTopic] = useState(null);
  const [topicLoading, setTopicLoading] = useState(false);
  const [difficulty, setDifficulty] = useState("random");
  const [selectedTags, setSelectedTags] = useState([]);
  const [topicFading, setTopicFading] = useState(false);

  // Frameworks state (9c)
  const [frameworks, setFrameworks] = useState([]);
  const [frameworksLoading, setFrameworksLoading] = useState(false);
  const [selectedFramework, setSelectedFramework] = useState(null);

  // Read Aloud elapsed time (9d)
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  // Load modes and find current mode by slug
  useEffect(() => {
    const fetchMode = async () => {
      try {
        const response = await api.get("/modes");
        const modes = Array.isArray(response.data) ? response.data : response.data.modes || [];
        const currentMode = modes.find((m) => m.slug === modeSlug);

        if (!currentMode) {
          toast.error("Mode not found", { autoClose: 2000, position: "top-center" });
          setTimeout(() => navigate("/overview"), 2000);
          return;
        }

        setMode(currentMode);
        setTimer(currentMode.default_timer_seconds || 60);
      } catch (err) {
        console.error("Failed to load mode:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMode();
  }, [modeSlug, navigate]);

  // Load frameworks (9c)
  useEffect(() => {
    const fetchFrameworks = async () => {
      setFrameworksLoading(true);
      try {
        const response = await api.get("/frameworks");
        setFrameworks(response.data.frameworks || []);
      } catch (err) {
        console.error("Failed to load frameworks:", err);
      } finally {
        setFrameworksLoading(false);
      }
    };

    fetchFrameworks();
  }, []);

  // Load initial topic (9b)
  useEffect(() => {
    if (!mode) return;
    fetchTopic();
  }, [mode]);

  // Fetch topic with current filters (9b)
  const fetchTopic = async () => {
    if (!mode) return;

    setTopicLoading(true);
    setTopicFading(true);

    try {
      let url = `/topics/random?mode=${mode.slug}`;
      if (difficulty !== "random") url += `&difficulty=${difficulty}`;
      if (selectedTags.length > 0) url += `&tags=${selectedTags.join(",")}`;

      const response = await api.get(url);
      setTopic(response.data);

      // Default framework from topic metadata if available
      if (response.data.meta?.suggested_framework) {
        setSelectedFramework(response.data.meta.suggested_framework);
      }

      // Fade in effect
      setTimeout(() => setTopicFading(false), 50);
    } catch (err) {
      console.error("Failed to load topic:", err);
      toast.error("Could not load topic", { autoClose: 2000, position: "top-center" });
    } finally {
      setTopicLoading(false);
    }
  };

  // Request microphone access
  useEffect(() => {
    const startMicrophone = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        setStream(mediaStream);
      } catch (err) {
        toast.error("❌ Microphone access denied!", { autoClose: 2000, position: "top-center" });
      }
    };

    startMicrophone();

    return () => {
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  // Timer countdown (normal modes) or count-up (read-aloud) (9d)
  useEffect(() => {
    if (!recording) return;

    const interval = setInterval(() => {
      if (displayMode.slug === "read-aloud") {
        // Count up for read-aloud mode
        setElapsedSeconds((prev) => prev + 1);
      } else {
        // Countdown for other modes
        setTimer((prev) => {
          if (prev <= 1) {
            stopRecording();
            return prev;
          }
          return prev - 1;
        });
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [recording, displayMode]);

  // Start recording
  const startRecording = () => {
    recordedChunksRef.current = [];

    if (!stream) {
      toast.error("Microphone not available!");
      return;
    }

    // Reset elapsed time for read-aloud mode
    if (displayMode.slug === "read-aloud") {
      setElapsedSeconds(0);
    }

    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        recordedChunksRef.current.push(e.data);
      }
    };

    mediaRecorder.start();
    setRecording(true);
    setPaused(false);
  };

  // Pause recording
  const pauseRecording = () => {
    mediaRecorderRef.current?.pause();
    setPaused(true);
  };

  // Resume recording
  const resumeRecording = () => {
    mediaRecorderRef.current?.resume();
    setPaused(false);
  };

  // Stop recording
  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
    setPaused(false);
  };

  // Delete recording
  const deleteRecording = () => {
    recordedChunksRef.current = [];
    setRecording(false);
    setPaused(false);
    toast.success("Recording deleted!", {
      position: "top-center",
      autoClose: 2000,
    });
  };

  // Submit recording
  const submitRecording = async () => {
    if (recordedChunksRef.current.length === 0) {
      toast.error("No recording available.");
      return;
    }

    setSubmitting(true);

    try {
      const blob = new Blob(recordedChunksRef.current, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("mode_id", mode?.id || 1);
      if (topic?.id) formData.append("topic_id", topic.id);
      if (selectedFramework) formData.append("framework_slug", selectedFramework);
      formData.append("video", blob, `recording-${Date.now()}.webm`);

      const response = await api.post("/recordings", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (!response.data || !response.data.id) {
        throw new Error("Invalid response from server");
      }

      setRecordingId(response.data.id);
      toast.success("🎉 Recording submitted!", {
        position: "top-center",
        autoClose: 2000,
      });

      setShowModal(true);
    } catch (err) {
      console.error("Submission failed:", err);
      toast.error("Submission failed. Try again.", { autoClose: 2000, position: "top-center" });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  const displayMode = mode || { name: "Practice", id: 1, default_timer_seconds: 60 };

  // Read Aloud mode uses count-up, others use countdown
  const isReadAloud = displayMode.slug === "read-aloud";
  const displayTimer = isReadAloud ? elapsedSeconds : timer;
  const timerSeconds = displayTimer % 60;
  const timerMinutes = Math.floor(displayTimer / 60);
  const isWarning = !isReadAloud && timer <= 10;

  return (
    <>
      <div className="flex flex-col h-screen max-h-screen overflow-hidden">
        {/* Header */}
        <div className="bg-[#FFEEE3] border border-[#FFEEE3]">
          <h1 className="ml-8 font-semibold text-[#F25019] text-xl my-6">
            {displayMode.name || "Practice"}
          </h1>
        </div>

        {/* Main Content Area - Scrollable */}
        <div className="flex-1 overflow-y-auto">
          <div className="flex flex-col items-center justify-start p-8 gap-8">
            {/* Timer Display */}
            <div className={`text-6xl font-bold font-mono transition-colors ${
              isWarning ? "text-red-600" : "text-gray-800"
            }`}>
              {timerMinutes.toString().padStart(2, "0")}:
              {timerSeconds.toString().padStart(2, "0")}
            </div>

            {/* Recording Status */}
            {recording && (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-red-600 rounded-full animate-pulse"></div>
                <p className="text-gray-600 font-medium">
                  {paused ? "Recording paused" : "Recording..."}
                </p>
              </div>
            )}

            {/* Microphone Indicator */}
            {!recording && recordedChunksRef.current.length === 0 && (
              <p className="text-gray-400 text-sm">
                🎤 Ready to record. Click the record button to start.
              </p>
            )}

            {/* Topic Card (9b) - Mode-Specific Rendering (9d) */}
            {!recording && topic && (
              <div className={`transition-opacity duration-400 w-full max-w-md ${
                topicFading ? "opacity-0" : "opacity-100"
              }`}>
                {/* Learn Vocabulary Mode (9d) */}
                {displayMode.slug === "learn-vocabulary" ? (
                  <div className="bg-white border-2 border-gray-200 rounded-lg p-6 shadow-md">
                    <p className="text-sm text-gray-500 uppercase tracking-wide mb-3">Vocabulary Word</p>
                    <div className="mb-4">
                      <p className="text-3xl font-bold text-[#F25019] mb-2">{topic.text}</p>
                      {topic.meta?.part_of_speech && (
                        <p className="text-sm text-gray-600 italic mb-2">
                          <span className="font-semibold">{topic.meta.part_of_speech}</span>
                        </p>
                      )}
                      {topic.meta?.definition && (
                        <p className="text-sm text-gray-700 mb-2">
                          <strong>Definition:</strong> {topic.meta.definition}
                        </p>
                      )}
                      {topic.meta?.example_sentence && (
                        <p className="text-sm text-gray-600 italic border-l-2 border-[#F25019] pl-3">
                          "{topic.meta.example_sentence}"
                        </p>
                      )}
                    </div>
                    <button
                      onClick={fetchTopic}
                      disabled={topicLoading}
                      className="w-full px-4 py-2 bg-[#F25019] text-white rounded-lg hover:bg-[#CC3C0C] disabled:opacity-50 transition-colors font-medium text-sm"
                    >
                      {topicLoading ? "Loading..." : "Get Different Word"}
                    </button>
                  </div>
                ) : displayMode.slug === "read-aloud" ? (
                  /* Read Aloud Mode (9d) */
                  <div className="bg-white border-2 border-gray-200 rounded-lg p-6 shadow-md">
                    <p className="text-sm text-gray-500 uppercase tracking-wide mb-3">Passage</p>
                    <div className="mb-4">
                      <p className="text-lg leading-relaxed text-gray-800 mb-3">
                        {topic.text}
                      </p>
                      {topic.meta?.target_seconds && (
                        <p className="text-sm text-gray-600">
                          Target time: <span className="font-semibold">{topic.meta.target_seconds}s</span>
                          {topic.meta?.word_count && (
                            <> ({topic.meta.word_count} words)</>
                          )}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={fetchTopic}
                      disabled={topicLoading}
                      className="w-full px-4 py-2 bg-[#F25019] text-white rounded-lg hover:bg-[#CC3C0C] disabled:opacity-50 transition-colors font-medium text-sm"
                    >
                      {topicLoading ? "Loading..." : "Get Different Passage"}
                    </button>
                  </div>
                ) : (
                  /* Default Mode (9d) */
                  <div className="bg-white border-2 border-gray-200 rounded-lg p-6 shadow-md">
                    <p className="text-sm text-gray-500 uppercase tracking-wide mb-2">Today's Topic</p>
                    <p className="text-xl font-semibold text-gray-800 mb-4">{topic.text}</p>

                    {topic.difficulty && (
                      <p className="text-xs text-gray-600 mb-3">
                        Difficulty: <span className="font-semibold capitalize">{topic.difficulty}</span>
                      </p>
                    )}

                    <button
                      onClick={fetchTopic}
                      disabled={topicLoading}
                      className="w-full px-4 py-2 bg-[#F25019] text-white rounded-lg hover:bg-[#CC3C0C] disabled:opacity-50 transition-colors font-medium text-sm"
                    >
                      {topicLoading ? "Loading..." : "Get Different Topic"}
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Difficulty Filter (9b) */}
            {!recording && (
              <div className="w-full max-w-md">
                <p className="text-sm text-gray-600 mb-2">Difficulty:</p>
                <div className="flex gap-2 flex-wrap">
                  {["easy", "medium", "hard", "random"].map((level) => (
                    <button
                      key={level}
                      onClick={() => {
                        setDifficulty(level);
                        fetchTopic();
                      }}
                      className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                        difficulty === level
                          ? "bg-[#F25019] text-white"
                          : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                      }`}
                    >
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Frameworks Accordion (9c) */}
            {!recording && frameworks.length > 0 && (
              <div className="w-full max-w-md">
                <p className="text-sm text-gray-600 mb-3">Speaking Framework:</p>
                <div className="space-y-2 border-t border-gray-200">
                  {frameworks.map((fw) => (
                    <Disclosure key={fw.slug}>
                      {({ open }) => (
                        <>
                          <Disclosure.Button className="flex w-full justify-between items-center px-4 py-3 text-left text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
                            <div className="flex items-center gap-2">
                              <input
                                type="radio"
                                name="framework"
                                checked={selectedFramework === fw.slug}
                                onChange={() => setSelectedFramework(fw.slug)}
                                className="w-4 h-4"
                              />
                              <span>{fw.name}</span>
                            </div>
                            <ChevronUpIcon
                              className={`w-5 h-5 transition-transform ${
                                open ? "transform rotate-180" : ""
                              }`}
                            />
                          </Disclosure.Button>

                          <Disclosure.Panel className="px-4 py-2 bg-gray-50 text-sm text-gray-600">
                            <p className="mb-3 text-xs text-gray-500">{fw.best_for}</p>
                            <ul className="space-y-2">
                              {fw.steps.map((step) => (
                                <li key={step.letter} className="text-xs">
                                  <strong className="text-[#F25019]">{step.letter}.</strong> {step.label}: {step.description}
                                </li>
                              ))}
                            </ul>
                          </Disclosure.Panel>
                        </>
                      )}
                    </Disclosure>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Privacy Disclaimer */}
        <div className="px-8 py-4 bg-blue-50 border-t border-blue-200">
          <p className="text-xs text-gray-600">
            🔒 <strong>Privacy:</strong> Your audio is transcribed and analyzed, then deleted.
            No recordings are stored on our servers.
          </p>
        </div>

        {/* Controls Footer */}
        <div className="p-6 py-8">
          {/* Control Row */}
          <div className="w-full flex items-center justify-between">
            {/* Left: Pause/Resume */}
            <div className="flex justify-start w-1/3">
              {recording && (
                <button
                  onClick={paused ? resumeRecording : pauseRecording}
                  className="w-16 h-16 rounded-full flex items-center justify-center shadow-lg border-4 border-white bg-white hover:shadow-xl transition-shadow"
                  title={paused ? "Resume" : "Pause"}
                >
                  {paused ? (
                    // Resume ▶
                    <div className="w-0 h-0 border-l-[20px] border-l-[#8F8D8D] border-t-[12px] border-t-transparent border-b-[12px] border-b-transparent"></div>
                  ) : (
                    // Pause ⏸
                    <div className="flex gap-1">
                      <div className="w-2 h-6 bg-[#8F8D8D]"></div>
                      <div className="w-2 h-6 bg-[#8F8D8D]"></div>
                    </div>
                  )}
                </button>
              )}
            </div>

            {/* Center: Record/Stop */}
            <div className="flex justify-center w-1/3">
              <button
                onClick={recording ? stopRecording : startRecording}
                disabled={submitting}
                className="w-20 h-20 rounded-full flex items-center justify-center shadow-lg border-4 border-white bg-white hover:shadow-xl transition-shadow disabled:opacity-50"
                title={recording ? "Stop" : "Start"}
              >
                {recording ? (
                  // Stop ⏹
                  <div className="w-10 h-10 bg-red-600 rounded"></div>
                ) : (
                  // Start 🔴
                  <div className="w-12 h-12 bg-red-600 rounded-full"></div>
                )}
              </button>
            </div>

            {/* Right: Delete + Submit */}
            <div className="flex justify-end w-1/3 gap-3">
              {recordedChunksRef.current.length > 0 && (
                <>
                  <button
                    onClick={deleteRecording}
                    disabled={submitting}
                    className="px-4 py-2 text-gray-500 hover:text-red-600 font-bold transition-colors disabled:opacity-50"
                    title="Delete"
                  >
                    Delete
                  </button>
                  <button
                    onClick={submitRecording}
                    disabled={submitting}
                    className="px-6 py-2 bg-[#F25019] text-white hover:bg-white hover:text-[#F25019] rounded-lg shadow font-bold transition-colors disabled:opacity-50"
                  >
                    {submitting ? "Transcribing..." : "Submit"}
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Success Modal */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
            <h2 className="text-xl font-semibold mb-4">🎉 Submission Successful</h2>
            <p className="mb-6 text-gray-700">
              Your recording has been transcribed and is being analyzed.
            </p>
            <div className="flex justify-center gap-4">
              <button
                onClick={() => {
                  setShowModal(false);
                  navigate("/overview");
                }}
                className="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400 font-medium transition-colors"
              >
                Back to Overview
              </button>
              <button
                onClick={() => {
                  navigate("/feedback");
                }}
                className="px-4 py-2 bg-[#F25019] text-white rounded-lg hover:bg-[#CC3C0C] font-medium transition-colors"
              >
                View Feedback
              </button>
            </div>
          </div>
        </div>
      )}

      <ToastContainer />
    </>
  );
};
