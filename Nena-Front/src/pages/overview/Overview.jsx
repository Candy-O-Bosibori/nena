import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import api from "../../api/api";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const Overview = () => {
  const [modes, setMode] = useState([]);
  const [activity_log, setActivity_log] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nextPractice, setNextPractice] = useState(null);
  const [nextPracticeLoading, setNextPracticeLoading] = useState(false);
  const [trends, setTrends] = useState(null);
  const [trendsLoading, setTrendsLoading] = useState(false);
  const [recordings, setRecordings] = useState([]);
  const navigate = useNavigate();
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    const refreshToken = localStorage.getItem('refreshToken');

    // Only fetch if user is authenticated
    if (!token || !refreshToken) {
      setLoading(false);
      return;
    }

    let userId;
    try {
      const decodedToken = jwtDecode(token);
      userId = decodedToken.sub;
    } catch (error) {
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        // fetch modes
        const response1 = await fetch("http://127.0.0.1:5000/modes", {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        const data1 = await response1.json();
        setMode(data1);

        // Activity log
        const response2 = await fetch("http://127.0.0.1:5000/activity_logs", {
          headers: { 'Authorization': 'Bearer ' + token }
        });

        const data2 = await response2.json();

        const response3 = await fetch(`http://127.0.0.1:5000/userById/${userId}`, {
          headers: { 'Authorization': 'Bearer ' + token }
        });

        const data3 = await response3.json();
        setActivity_log(data2);
        setUser(data3);

      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    // Fetch next practice (9h - continue block)
    const fetchNextPractice = async () => {
      setNextPracticeLoading(true);
      try {
        const response = await api.get('/next-practice');
        setNextPractice(response.data);
      } catch (err) {
        // Silently fail if not authenticated
        setNextPractice(null);
      } finally {
        setNextPracticeLoading(false);
      }
    };

    // Fetch trends (9j - sparklines)
    const fetchTrends = async () => {
      setTrendsLoading(true);
      try {
        const response = await api.get('/trends');
        setTrends(response.data);
      } catch (err) {
        // Silently fail if not authenticated
        setTrends(null);
      } finally {
        setTrendsLoading(false);
      }
    };

    // Fetch recordings for count check (9j - gating)
    const fetchRecordings = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/recordings', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        setRecordings(data);
      } catch (err) {
        // Silently fail if not authenticated
        setRecordings([]);
      }
    };

    fetchData();
    fetchNextPractice();
    fetchTrends();
    fetchRecordings();
  }, []);

    return (
    <div className=" px-4 lg:px-[50px] px-4 lg:py-[20px]min-h-screen bg-white py-10 flex flex-col md:flex-row gap-6">
      {/* LEFT SIDE - CARDS */}
      <div className="md:w-3/5 flex flex-col gap-6 mr-4"      
      >
        <h1 className="text-lg md:text-xl  text-[#F25019] -mb-6">
          Hello <span className="text-[#F25019] font-bold">{user.name}</span>. Welcome !!
        </h1>

        {/* Continue Block (9h) */}
        {nextPractice && (
          <div
            className="rounded-2xl text-white p-5 md:p-6 shadow-lg w-full min-h-[120px] flex flex-col justify-center cursor-pointer transition-transform hover:scale-105"
            style={{
              backgroundColor: nextPractice.mode?.accent_color || "#F25019",
              boxShadow: `0 10px 25px ${nextPractice.mode?.accent_color || "#F25019"}40`
            }}
            onClick={() => navigate(`/practice/${nextPractice.mode?.slug}`)}
          >
            <p className="text-xs opacity-90 mb-1">👉 Continue where you left off</p>
            <h3 className="font-semibold text-base md:text-lg mb-2">{nextPractice.topic?.text}</h3>
            <p className="text-sm opacity-90">{nextPractice.reason}</p>
          </div>
        )}

        <h2 className="text-sm md:text-2xl -mb-2 ">Select A Mode</h2>

        {/* Dynamic Mode Cards (9h) */}
        {modes.map((mode) => (
          <div
            key={mode.id}
            className="rounded-2xl text-white p-5 md:p-6 shadow-lg w-full min-h-[150px] flex flex-col justify-center cursor-pointer transition-transform hover:scale-105"
            style={{
              backgroundColor: mode.accent_color || "#F25019",
              boxShadow: `0 10px 25px ${mode.accent_color || "#F25019"}40`
            }}
            onClick={() => navigate(`/practice/${mode.slug}`)}
          >
            <h3 className="font-semibold text-base md:text-lg md:-mt-8">{mode.name}</h3>
            <p className="text-sm mt-2">{mode.description}</p>
          </div>
        ))}
      </div>

      {/* RIGHT SIDE - STATISTICS + ACTIVITY */}
      <div className="md:w-2/5 flex flex-col gap-6">
        {/* Statistics */}
        <div className=" flex flex-col justify-center">
          <h2 className="text-lg md:text-2xl mb-4">Statistics</h2>
          <div className="grid grid-cols-2 gap-4">
            {/* Stat Box */}
            <div className="bg-[#FFEEE3]  md:min-h-40 rounded-xl p-4 flex flex-col items-center justify-center shadow-sm">
              <span className="text-sm">{modes[0]?.name}</span>
              <span className="text-2xl font-bold text-red-500 mt-2">{modes[0]?.recordings.length}</span>
            </div>
            <div className="bg-[#FFEEE3]  md:min-h-40 rounded-xl p-4 flex flex-col items-center justify-center shadow-sm">
              <span className="text-sm">{modes[1]?.name}</span>
              <span className="text-2xl font-bold text-red-500 mt-2">{modes[1]?.recordings.length}</span>
            </div>
            <div className="bg-[#FFEEE3]   md:min-h-40 rounded-xl p-4 flex flex-col items-center justify-center shadow-sm">
              <span className="text-sm">{modes[2]?.name}</span>
              <span className="text-2xl font-bold text-red-500 mt-2">{modes[2]?.recordings.length}</span>
            </div>
            <div className="bg-[#FFEEE3]  md:min-h-40  rounded-xl p-4 flex flex-col items-center justify-center shadow-sm">
              <span className="text-sm">{modes[3]?.name}</span>
              <span className="text-2xl font-bold text-red-500 mt-2">{modes[3]?.recordings.length}</span>
            </div>
          </div>
        </div>

        {/* Activity */}
      <div className="h-[350px] flex flex-col justify-between pb-10">
        <h2 className="text-lg md:text-xl font-bold mb-4">Total day recording</h2>

        <div className="flex items-end  justify-between h-40 px-2">
          {activity_log.map((entry, idx) => {
            // 📊 Bar scaling
            const maxHeight = 250;
            const maxTime = Math.max(...activity_log.map(e => e.time_spent_minutes || 0));
            let barHeight = 0;

            if (maxTime > 0) {
              barHeight = Math.round((entry.time_spent_minutes || 0) / maxTime * maxHeight);
            }

            // 🔹 Ensure ALL bars are visible (even 0 minutes)
            const minBarHeight = 5; 
            if (barHeight < minBarHeight) {
              barHeight = minBarHeight;
            }

          const time=(Math.round(entry.time_spent_minutes)/60).toFixed(1)
          const [year, month, day] = entry.date.split("-").map(Number);
          const entryDate = new Date(year, month - 1, day); // month is 0-indexed
          const dayName = entryDate.toLocaleDateString("en-US", { weekday: "short" });

            // 🔥 Check if this entry is today (local-safe)
            const today = new Date();
            const todayStr = today.getFullYear() + "-" +

              String(today.getMonth() + 1).padStart(2, "0") + "-" +
              String(today.getDate()).padStart(2, "0");
            
            const isToday = entry.date === todayStr;

            return (
              <div key={idx} className="flex flex-col items-center">
                {/* Bar */}
                <div
                  style={{ height: `${barHeight}px` }}
                  className={`w-6 rounded-lg transition-all duration-300 
                    ${isToday ? "bg-[#F25019] shadow-md" : "bg-[#FFEEE3]"}`}
                ></div>

                {/* Label */}
                <span className={`text-xs mt-1 ${isToday ? "font-bold text-[#F25019]" : "text-gray-500"}`}>
                  {isToday ? "Today" : dayName}
                </span>
                <span className={`text-xs mt-1 ${isToday ? "font-bold text-[#F25019]" : "text-gray-500"}`}>
                  {`${time}m`}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Trends Sparklines (9j) */}
      {recordings.length >= 3 && trends?.trends && (
        <div className="flex flex-col gap-2">
          <h2 className="text-lg md:text-xl font-bold mb-2">30-Day Trends</h2>

          {/* Pace Chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-600 mb-2">Pace (WPM)</p>
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={trends.trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={["dataMin - 10", "dataMax + 10"]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(value) => value.toFixed(1)} />
                <Line type="monotone" dataKey="pace_wpm_avg" stroke="#F25019" isAnimationActive={false} dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
            {trends.summary && (
              <p className="text-xs text-gray-600 mt-1">
                Avg: {trends.summary.pace_wpm_avg?.toFixed(1)} WPM
                {trends.trends[0]?.pace_wpm_avg && trends.trends[trends.trends.length - 1]?.pace_wpm_avg && (
                  trends.trends[trends.trends.length - 1].pace_wpm_avg > trends.trends[0].pace_wpm_avg ? " ▲" : " ▼"
                )}
              </p>
            )}
          </div>

          {/* Fillers Chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-600 mb-2">Filler Words</p>
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={trends.trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, "dataMax + 1"]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(value) => value.toFixed(1)} />
                <Line type="monotone" dataKey="filler_words_avg" stroke="#EF4444" isAnimationActive={false} dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
            {trends.summary && (
              <p className="text-xs text-gray-600 mt-1">
                Avg: {trends.summary.filler_words_avg?.toFixed(1)}
                {trends.trends[0]?.filler_words_avg && trends.trends[trends.trends.length - 1]?.filler_words_avg && (
                  trends.trends[trends.trends.length - 1].filler_words_avg < trends.trends[0].filler_words_avg ? " ▼" : " ▲"
                )}
              </p>
            )}
          </div>

          {/* Hedges Chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-600 mb-2">Hedges</p>
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={trends.trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, "dataMax + 1"]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(value) => value.toFixed(1)} />
                <Line type="monotone" dataKey="hedge_count_avg" stroke="#F59E0B" isAnimationActive={false} dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
            {trends.summary && (
              <p className="text-xs text-gray-600 mt-1">
                Avg: {trends.summary.hedge_count_avg?.toFixed(1)}
                {trends.trends[0]?.hedge_count_avg && trends.trends[trends.trends.length - 1]?.hedge_count_avg && (
                  trends.trends[trends.trends.length - 1].hedge_count_avg < trends.trends[0].hedge_count_avg ? " ▼" : " ▲"
                )}
              </p>
            )}
          </div>

          {/* Concreteness Chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-600 mb-2">Concreteness (%)</p>
            <ResponsiveContainer width="100%" height={100}>
              <LineChart data={trends.trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, 1]} tick={{ fontSize: 10 }} tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                <Tooltip formatter={(value) => `${(value * 100).toFixed(0)}%`} />
                <Line type="monotone" dataKey="concreteness_ratio_avg" stroke="#10B981" isAnimationActive={false} dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
            {trends.summary && (
              <p className="text-xs text-gray-600 mt-1">
                Avg: {(trends.summary.concreteness_ratio_avg * 100)?.toFixed(0)}%
                {trends.trends[0]?.concreteness_ratio_avg && trends.trends[trends.trends.length - 1]?.concreteness_ratio_avg && (
                  trends.trends[trends.trends.length - 1].concreteness_ratio_avg > trends.trends[0].concreteness_ratio_avg ? " ▲" : " ▼"
                )}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Placeholder if not enough recordings (9j) */}
      {recordings.length < 3 && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
          <p className="text-sm text-gray-600">Complete 3+ recordings to see 30-day trends</p>
        </div>
      )}
      </div>
    </div>
  );
}
