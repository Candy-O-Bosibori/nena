import React, { useEffect, useRef, useState } from "react";

/**
 * Slot-reel topic reveal.
 *
 * While the real topic request is in flight, placeholder lines cycle at a
 * decelerating cadence. The reel is masked top and bottom so neighbouring lines
 * fade out, giving the impression of a wheel coming to rest.
 */
const SpinReveal = ({
  candidates = [],
  resolve = async () => ({}),
  renderResult = () => null,
  onSettle = () => {},
  onError = () => {},
  spinKey = "",
  accent = "#DC9750",
}) => {
  const [displayedText, setDisplayedText] = useState("");
  const [topic, setTopic] = useState(null);
  const [settled, setSettled] = useState(false);
  const [cycling, setCycling] = useState(false);
  const [error, setError] = useState(null);

  const tickIndexRef = useRef(0);
  const timeoutRef = useRef(null);
  const delays = [80, 80, 90, 100, 120, 140, 170, 210, 260, 320, 400];

  useEffect(() => {
    if (!spinKey) return;

    setSettled(false);
    setTopic(null);
    setError(null);
    setCycling(true);
    tickIndexRef.current = 0;
    setDisplayedText(candidates[0] || "Loading…");

    const scheduleNextTick = (index) => {
      const delay = delays[Math.min(index, delays.length - 1)];
      timeoutRef.current = setTimeout(() => {
        tickIndexRef.current += 1;
        if (candidates.length) {
          setDisplayedText(candidates[tickIndexRef.current % candidates.length]);
        }
        scheduleNextTick(tickIndexRef.current);
      }, delay);
    };

    scheduleNextTick(1);

    resolve()
      .then((result) => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setTopic(result);
        setCycling(false);
        setSettled(true);
        setError(null);
        onSettle(result);
      })
      .catch((err) => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setCycling(false);
        setError(err?.response?.data?.error || "Couldn't load a topic — try again");
        onError(err);
      });

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [spinKey]);

  // Ghost lines above/below the active one, so the reel reads as a wheel.
  const ghost = (offset) => {
    if (!candidates.length) return "";
    const i = (tickIndexRef.current + offset + candidates.length * 4) % candidates.length;
    return candidates[i];
  };

  return (
    <div className="relative w-full">
      {/* Hairlines mark the reel window */}
      <div className="border-y border-line/80">
        <div className="relative flex min-h-[190px] items-center justify-center px-6 py-8 md:min-h-[210px]">
          {error ? (
            <div className="text-center">
              <p className="text-sm font-semibold text-danger">{error}</p>
              <p className="mt-1.5 text-xs text-ink-muted">Press Spin to try again</p>
            </div>
          ) : settled && topic ? (
            renderResult(topic, settled)
          ) : (
            <div className="w-full select-none text-center" aria-live="polite">
              {/* faded neighbour above */}
              <p className="truncate text-base font-medium text-ink-muted/30">
                {ghost(-1)}
              </p>
              <p
                className="font-display my-2 truncate text-2xl font-normal tracking-tight md:text-3xl"
                style={{ color: accent }}
              >
                {displayedText}
              </p>
              {/* faded neighbour below */}
              <p className="truncate text-base font-medium text-ink-muted/30">
                {ghost(1)}
              </p>
            </div>
          )}
        </div>
      </div>

      {cycling && (
        <span className="sr-only" role="status">
          Choosing a topic…
        </span>
      )}
    </div>
  );
};

export default SpinReveal;
