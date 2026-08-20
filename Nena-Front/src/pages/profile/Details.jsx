import React from 'react'
import { CiEdit } from "react-icons/ci";

export const Details = ({user, setShowNameModal,setShowPasswordModal, setShowContactModal,  setShowImageModal,  setShowEmailModal}) => {
  return (
    <div className="px-5 ">
    <div className=" mb-5">Your Profile</div>

    <div className="flex space-x-5">

      <label htmlFor="" className="font-light  w-1/2 "><span className="text-[11px] font-medium">Name</span>
      <div className="bg-gray-100 with mt-2 full flex justify-between px-2 py-1 rounded ">
        <div className="text-Variant2 text-sm md:text-base">{user.name}</div> <CiEdit  onClick={() => { setShowNameModal(true)}} className=" w-4 h-4"/>
      </div>
      </label>
      <label htmlFor="" className="font-light  w-1/2"><span className="text-[11px] font-medium">Image</span>
      <div className="bg-gray-100 with mt-2 full flex justify-between px-2 py-1 rounded ">
      <div className="text-Variant2 text-sm md:text-base">Upload a new image</div> <CiEdit  onClick={() => {setShowImageModal(true)}} className=" w-4 h-4"/>
      </div>
      </label>

    </div>
         <div className="flex space-x-5 mt-3">

      <label htmlFor="" className="font-light  w-1/2 "><span className="text-[11px] font-medium">Email</span>
      <div className="bg-gray-100 with mt-2 full flex justify-between px-2 py-1 rounded ">
        <div className="text-Variant2 text-sm md:text-base">{user.email}</div> <CiEdit onClick={() => { setShowEmailModal(true)}} className=" w-4 h-4"/>
      </div>
      </label>
      <label htmlFor="" className="font-light w-1/2"><span className="text-[11px] font-medium">Password</span>
      <div className="bg-gray-100 with mt-2 full flex justify-between px-2 py-1 rounded ">
      <div className="text-Variant2 text-sm md:text-base">Change your password</div> <CiEdit onClick={() => {setShowPasswordModal(true)}}className=" w-4 h-4"/>
      </div>
      </label>
     
    </div>

    <div className="mt-2"> 
   
      
    </div>
    
    
  </div>
  )
}