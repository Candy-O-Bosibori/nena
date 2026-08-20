import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import logo from "../../assets/logo.png";
import image from "../../assets/image.png";
import { jwtDecode } from 'jwt-decode';
import { CiHome } from "react-icons/ci";
import { CiVideoOn } from "react-icons/ci";
import { CiViewList } from "react-icons/ci";
import { CiUser } from "react-icons/ci";
import { NavLink } from "react-router-dom";


export const SideBar = () => {
    const navigate = useNavigate();
    const [employee, setEmployee] = useState(null);
    

    useEffect(() => {
    const token = localStorage.getItem('token');
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    fetch('http://127.0.0.1:5000/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => response.json())
      .then(data => {
        const user = data.find(user => user.id === userId);
        setEmployee(user);
      })
      .catch(error => console.error('Error:', error));
    }, []);

    const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("refreshToken");
  navigate("/signin");
};


  return (
    <div className=' bg-[#FFEEE3] 
     text-[#8F8D8D] w-full
     h-[100vh] flex flex-col p-[20px]
      justify-between  font-body m-0
       text-center lg:text-left items-center
        lg:items-start  '>
      <div className=' ml-10 gap-[50px] '>
        <div className='mt-10 flex flex-col items-center gap-[20px]'>
          <img src={logo } alt="logo" className=" w-[130px] max-h-[64px] max-w-full px-4" />
        </div>
        <div className='flex flex-col gap-[20px] py-[30px] '>
          
            
          <div>
            <ul className='flex flex-col gap-[25px] my-10'>
  <li className="relative">
    <NavLink to="/overview">
    {({ isActive }) => (
      <div className={`flex items-center  ${isActive ? "text-[#F25019]" : "text-[#8F8D8D]"} hover:text-[#F25019]`}>
        <CiHome className="h-5 w-5 mr-5" />
        <span className="text-[15px]">Overview</span>

        {/* Orange dot, absolutely positioned relative to li */}
        {isActive && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F25019] hidden md:block "  />
        )}
      </div>
    )}
  </NavLink>
  </li>
  <li className="relative">
    <NavLink to="/recording">
    {({ isActive }) => (
      <div className={`flex items-center  ${isActive ? "text-[#F25019]" : "text-[#8F8D8D]"} hover:text-[#F25019]`}>
        <CiVideoOn className="h-5 w-5 mr-5" />
        <span className="text-[15px]">Record</span>

        {/* Orange dot, absolutely positioned relative to li */}
        {isActive && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F25019] hidden md:block " />
        )}
      </div>
    )}
  </NavLink>
  </li>
  <li className="relative">
    <NavLink to="/feedback">
    {({ isActive }) => (
      <div className={`flex items-center  ${isActive ? "text-[#F25019]" : "text-[#8F8D8D]"} hover:text-[#F25019]`}>
        <CiViewList className="h-5 w-5 mr-5" />
        <span className="text-[15px]">Feedback</span>

        {/* Orange dot, absolutely positioned relative to li */}
        {isActive && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F25019] hidden md:block " />
        )}
      </div>
    )}
  </NavLink>
  </li>
  
  {/* <li className="relative">
    <NavLink to="/profile">
    {({ isActive }) => (
      <div className={`flex items-center  ${isActive ? "text-[#F25019]" : "text-[#8F8D8D]"} hover:text-[#F25019]`}>
        <CiUser className="h-5 w-5 mr-5" />
        <span className="text-[15px]">Profile</span>

        {isActive && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F25019] hidden md:block " />
        )}
      </div>
    )}
  </NavLink>
  </li> */}

  <li className="relative">
    <NavLink to="/vocab">
    {({ isActive }) => (
      <div className={`flex items-center  ${isActive ? "text-[#F25019]" : "text-[#8F8D8D]"} hover:text-[#F25019]`}>
        <CiUser className="h-5 w-5 mr-5" />
        <span className="text-[15px]">Vocabulary</span>

        {/* Orange dot, absolutely positioned relative to li */}
        {isActive && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F25019] hidden md:block " />
        )}
      </div>
    )}
  </NavLink>
  </li>
  
</ul>
          </div>
        </div>
      </div>
      <div className=' pl-10 p-[5px] flex flex-col gap-[25px] text-center lg:text-left items-center lg:items-start'>
        <div className=' flex flex-col '>
            <div>
                <img src={image} alt="" className='h-52 md:h-32 mb-4' />
            </div>
             <div className=" flex flex-col gap-3">
  <button
    onClick={handleLogout}
    className="flex items-center justify-center gap-2 px-4 py-2 bg-[#F25019] text-white rounded-lg shadow-md hover:bg-red-600"
  >
    Sign Out
  </button>
</div>
          {/* {employee ? (
            <div className='flex gap-[15px] p-[10px]'>
              <div className="w-[50px] h-[50px] overflow-hidden rounded-full">
                <img src={employee.image} alt={employee.name} className="w-full h-full object-cover" />
              </div>
              <div className='flex flex-col gap-[8px]'>
                <h1 className='text-[16px] font-bold text-Heading dark:text-primary-light'>{employee.name}</h1>
                <h1 className='text-[11px] font-bold text-Heading dark:text-primary-light'>{employee.department}</h1>
              </div>

            </div>
          ) : (
            <div>
              <p className='text-secondary text-sm'>Loading...</p>
            </div>
          )} */}
        </div>
        {/* <div className='flex gap-[30px]'>
         
          <button className='bg-secondary text-black hover:cursor-pointer hover:text-white px-[10px] py-[5px] rounded-[5px] text-[15px]' onClick={handleLogout}>Logout</button>
        </div> */}
      </div>
     
    </div>
  );
}
