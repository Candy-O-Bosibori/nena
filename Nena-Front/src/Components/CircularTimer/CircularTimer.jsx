import React, { forwardRef, useImperativeHandle, useRef, useState, useEffect } from "react";

const MAX_CANDLE_H = 170;
const MIN_CANDLE_H = 14;

/**
 * Candle timer.
 *
 * The candle's height tracks remaining/total, so it burns down over the full
 * duration no matter what that duration is. Adjusting by +/-0:30 changes the
 * total, which changes how much wax each second consumes -- a longer timer
 * burns visibly slower, a shorter one faster.
 *
 * In countup mode (read-aloud) there is no fixed end, so the candle fills
 * toward the mode's target duration instead of burning down.
 */
const CircularTimer = forwardRef(
  (
    {
      durationSeconds = 60,
      mode = "countdown",
      onComplete,
      onTick,
      accentColor = "#DC9750",
      warningThresholdSeconds = 10,
      midThresholdRatio = 0.5,
    },
    ref
  ) => {
    const [total, setTotal] = useState(durationSeconds);
    const [remaining, setRemaining] = useState(durationSeconds);
    const [elapsed, setElapsed] = useState(0);
    const [running, setRunning] = useState(false);
    const [paused, setPaused] = useState(false);
    const [completed, setCompleted] = useState(false);

    const intervalRef = useRef(null);

    const isCountdown = mode === "countdown";
    const displayValue = isCountdown ? remaining : elapsed;

    // Fraction of candle left. Countdown burns down from full; countup grows
    // toward the target so there's still a visual sense of progress.
    const progressRatio = isCountdown
      ? total > 0
        ? remaining / total
        : 0
      : Math.min(elapsed / (durationSeconds || 60), 1);

    const candleHeight =
      MIN_CANDLE_H + (MAX_CANDLE_H - MIN_CANDLE_H) * (isCountdown ? progressRatio : 1 - progressRatio);

    // Text color: accent while healthy, a darker primary shade past the
    // midpoint, danger red only in the final countdown seconds.
    let textColor = "text-ink";
    if (isCountdown) {
      if (
        progressRatio <= midThresholdRatio &&
        progressRatio > warningThresholdSeconds / (total || 1)
      ) {
        textColor = "text-primary-700";
      } else if (remaining <= warningThresholdSeconds) {
        textColor = "text-danger";
      }
    }

    const formatTime = (seconds) => {
      const s = Math.max(0, Math.ceil(seconds));
      const mins = Math.floor(s / 60);
      const secs = s % 60;
      return `${mins}:${secs.toString().padStart(2, "0")}`;
    };

    // Keep the latest callbacks in refs so the interval effect doesn't need them
    // as dependencies (which would tear down and restart the timer whenever the
    // parent re-renders and passes new function identities).
    const onCompleteRef = useRef(onComplete);
    const onTickRef = useRef(onTick);
    useEffect(() => {
      onCompleteRef.current = onComplete;
      onTickRef.current = onTick;
    });

    // Timer interval logic.
    // State updater functions must stay pure: React may call them during render,
    // so firing onComplete()/onTick() inside one would set state on the parent
    // mid-render ("Cannot update a component while rendering a different one").
    // The updaters below only compute the next value; side effects run in the
    // effect underneath, after the commit.
    useEffect(() => {
      if (!running || paused) return;

      intervalRef.current = setInterval(() => {
        if (isCountdown) {
          setRemaining((prev) => (prev <= 0 ? 0 : prev - 1));
        } else {
          setElapsed((prev) => prev + 1);
        }
      }, 1000);

      return () => clearInterval(intervalRef.current);
    }, [running, paused, isCountdown]);

    // Report ticks after the value is committed, not from inside the updater.
    useEffect(() => {
      if (!running || paused) return;
      onTickRef.current?.(isCountdown ? remaining : elapsed);
    }, [remaining, elapsed, running, paused, isCountdown]);

    // Completion: countdown reaching zero is the only auto-complete path.
    useEffect(() => {
      if (!isCountdown || !running || remaining > 0) return;
      setRunning(false);
      setCompleted(true);
      onCompleteRef.current?.();
    }, [remaining, running, isCountdown]);

    // Imperative API
    useImperativeHandle(ref, () => ({
      start: () => {
        // Starting a finished timer restarts it, rather than immediately
        // re-firing completion because `remaining` is still 0.
        setCompleted(false);
        setElapsed(0);
        if (isCountdown) {
          setRemaining((prev) => (prev <= 0 ? total : prev));
        }
        setPaused(false);
        setRunning(true);
      },
      pause: () => {
        setPaused(true);
      },
      resume: () => {
        setPaused(false);
      },
      reset: () => {
        setRunning(false);
        setPaused(false);
        setRemaining(total);
        setElapsed(0);
        setCompleted(false);
      },
      adjust: (deltaSeconds) => {
        // Guard inside the updater so it reads current state, not the value
        // captured when this handle was created.
        setRemaining((prev) => Math.max(0, prev + deltaSeconds));
      },
    }));

    // Adjusting before the timer starts changes the total duration, which is
    // what makes the candle burn slower/faster -- not just its starting height.
    const adjustTotal = (delta) => {
      setCompleted(false);
      setTotal((prevTotal) => {
        const next = Math.max(30, Math.min(600, prevTotal + delta));
        setRemaining(next);
        return next;
      });
    };

    const flameVisible = isCountdown ? remaining > 0 : true;

    return (
      <div className="flex flex-col items-center justify-center gap-8">
        {/* Time display */}
        <div className="flex flex-col items-center">
          {completed ? (
            <span className="text-sm font-bold uppercase tracking-[0.16em] text-ink-soft">
              Time&rsquo;s up
            </span>
          ) : (
            <>
              <span
                className={`tabular text-5xl font-extrabold tracking-tight transition-colors duration-300 ${textColor}`}
              >
                {formatTime(displayValue)}
              </span>
              <span className="mt-1 text-[10px] font-bold uppercase tracking-[0.18em] text-ink-muted">
                {isCountdown ? "remaining" : "elapsed"}
              </span>
            </>
          )}
        </div>

        {/* Candle */}
        <div className="relative flex h-[220px] w-[120px] items-end justify-center">
          {/* Flame */}
          {flameVisible && (
            <div
              className="candle-flame absolute left-1/2 h-[26px] w-[16px] rounded-[50%_50%_50%_50%/60%_60%_40%_40%]"
              style={{
                bottom: candleHeight + 7,
                background:
                  "radial-gradient(circle at 50% 30%, #fff6c8, #ffb347 55%, #e0713c 100%)",
                boxShadow: "0 0 14px 4px rgba(255,170,60,.5)",
              }}
            />
          )}

          {/* Wick */}
          <div
            className="absolute left-1/2 h-[8px] w-[2px] -translate-x-1/2 bg-[#3a2e20]"
            style={{ bottom: candleHeight }}
          />

          {/* Candle body — tinted with the mode's accent so it matches the
              rest of the page rather than sitting outside the palette. */}
          <div
            className="w-[46px] rounded-t-[4px] rounded-b-[2px]"
            style={{
              height: candleHeight,
              background: `linear-gradient(90deg, ${accentColor}33, ${accentColor}18 50%, ${accentColor}33), linear-gradient(90deg, #f2e4c4, #fff7e2 50%, #f2e4c4)`,
              boxShadow: "inset -4px 0 6px rgba(0,0,0,.06)",
              transition: "height .2s linear",
            }}
          />
        </div>

        {/* ±0:30 Adjust buttons (countdown only, before the timer starts) */}
        {isCountdown && !running && !completed && (
          <div className="flex gap-4">
            <button
              onClick={() => adjustTotal(-30)}
              className="rounded-full border border-line bg-surface px-4 py-2 text-sm font-semibold text-ink-soft transition-all duration-200 hover:border-ink-muted hover:text-ink active:scale-95 focus-ring"
            >
              −0:30
            </button>
            <button
              onClick={() => adjustTotal(30)}
              className="rounded-full border border-line bg-surface px-4 py-2 text-sm font-semibold text-ink-soft transition-all duration-200 hover:border-ink-muted hover:text-ink active:scale-95 focus-ring"
            >
              +0:30
            </button>
          </div>
        )}
      </div>
    );
  }
);

CircularTimer.displayName = "CircularTimer";

export default CircularTimer;
