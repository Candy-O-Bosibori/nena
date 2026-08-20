import React, { useEffect, useRef, useState } from "react";
import { CiTrash } from "react-icons/ci";
import { useLocation, useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export const Recording = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { modeId, modeName } = location.state || {};

  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  const [stream, setStream] = useState(null);
  const [recording, setRecording] = useState(false);
  const [paused, setPaused] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [showPermissionNotice, setShowPermissionNotice] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [recordingId, setRecordingId] = useState(null);

  // Redirect if no mode selected
  useEffect(() => {
    if (!modeId) {
      toast.error("⚠️ Please select a mode first!", { autoClose: 2000 , position: "top-center",
      });

      setTimeout(() => navigate("/overview"), 2000);
    }
  }, [modeId, navigate]);

  if (!modeId) return <ToastContainer />; 


  // Access camera
  useEffect(() => {
      const startCamera = async () => {
        try {
          const mediaStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true,
          });
          videoRef.current.srcObject = mediaStream;
          setStream(mediaStream);
          setShowPermissionNotice(false);
        } catch (err) {
          toast.error("❌ Camera/microphone access denied!");
        }
      };
    startCamera();

    return () => {
      stream?.getTracks().forEach((track) => track.stop());
    };
  }, []);


  // Start recording
const startRecording = () => {
  setRecordedChunks([]); // clear any previous chunks

  if (!stream) {
    toast.error("Camera/microphone not available!");
    return;
  }

  const mediaRecorder = new MediaRecorder(stream);
  mediaRecorderRef.current = mediaRecorder;

  mediaRecorder.ondataavailable = (e) => {
    if (e.data.size > 0) {
      setRecordedChunks((prev) => [...prev, e.data]);
    }
  };

  mediaRecorder.start();
  setRecording(true);
  setPaused(false);

  mediaRecorder.onstop = () => {
    // Ensure final blob is complete after stopping
    if (recordedChunks.length > 0) {
      const finalBlob = new Blob(recordedChunks, { type: "video/webm" });
      setRecordedChunks([finalBlob]); // overwrite previous chunks with final blob
    }
  };
};

  // Pause / resume
  const pauseRecording = () => {
    mediaRecorderRef.current?.pause();
    setPaused(true);
  };

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

const deleteRecording = () => {
  setRecordedChunks([]);
  setRecording(false);
  setPaused(false);

  toast.success("Recording deleted!", {
    position: "top-center",
    autoClose: 2000,
  });
};

// Submit recording
const submitRecording = async () => {
  if (recordedChunks.length === 0) {
    alert("No recording available.");
    return;
  }

  setSubmitting(true);
  const token = localStorage.getItem("token");

  // Use the final blob (guaranteed complete)
  const blob = recordedChunks[0];
  const formData = new FormData();
  formData.append("mode_id", modeId);
  formData.append("video", blob, `recording-${Date.now()}.webm`);

  try {
    const response = await fetch("http://127.0.0.1:5000/recordings", {
      headers: { Authorization: "Bearer " + token },
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Failed to submit recording");

    const data = await response.json();
    toast.success("🎉 Video successfully submitted!", {
      position: "top-center",
      autoClose: 2000,
    });

    // Optionally save the returned video URL for playback
    // setRecordingId(data.id); or save data.video_url

    setShowModal(true);
  } catch (err) {
    console.error(err);
    alert("Submission failed. Try again.");
  } finally {
    setSubmitting(false);
  }
};

return (
  <>
<div className="flex flex-col h-screen max-h-screen overflow-hidden">

  {/* Recording / Header */}
  <div className="">
    <div className="bg-[#FFEEE3] border border-[#FFEEE3]   ">
     <h1 className=" ml-8 font-semibold text-[#F25019] text-xl my-6 text-lg md:text-xl  text-[#F25019] ">
       {modeName || "Recording"}
     </h1>
     </div>
  </div>

  {/* Video Area */}
  <div className="flex-1 flex items-center justify-center p-2 min-h-0">
    <video
      ref={videoRef}
      className="w-full h-full object-contain rounded "
      autoPlay
      muted
    />
  </div>

  {/* Footer / Controls */}
  <div className=" p-2 py-5 ">
     {/* Controls Row */}
     <div className="w-full   self-end  flex items-center justify-between ">
       {/* Left: Pause/Resume */}
       <div className="flex justify-start w-1/3">
         {recording && (
           <button
             onClick={paused ? resumeRecording : pauseRecording}
             className="w-16 h-16 rounded-full flex items-center justify-center shadow-lg border-4 border-white bg-white"
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
       {/* Center: Record / Stop */}
       <div className="flex justify-center w-1/3">
         <button
           onClick={recording ? stopRecording : startRecording}
           className="w-20 h-20 rounded-full flex items-center justify-center shadow-lg border-4 border-white bg-white"
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
         {recordedChunks.length > 0 && (
           <>
             
               
               <CiTrash
  onClick={deleteRecording}
  className="w-10 h-10 text-gray-500 hover:text-red-600 cursor-pointer ml-5"
/>
             <button
               onClick={submitRecording}
               disabled={submitting}
               className="px-4 py-2 bg-[#F25019] text-white hover:bg-white hover:text-[#F25019] rounded-lg shadow  font-bold"
             >
               {submitting ? "Submitting..." : "Submit"}
             </button>
           </>
         )}
       </div>
     </div>
  </div>
</div>
{showModal && (
  <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
      <h2 className="text-xl font-semibold mb-4">🎉 Submission Successful</h2>
      <p className="mb-4">Would you like to see the feedback on your video!</p>
      <div className="flex justify-center gap-4">
        <button
          onClick={() => {
              setShowModal(false);
              navigate("/overview"); // <-- replace with your actual route
            }}
          
          className="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400"
        >
          Close
        </button>
        <button
          onClick={() => navigate("/feedback")}
          className="px-4 py-2 bg-[#F25019] text-white rounded-lg hover:bg-white hover:text-[#F25019]"
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
}