import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { PiEyeLight } from "react-icons/pi";
import { PiEyeSlash } from "react-icons/pi";
import logo from "../../assets/logo.png";
import github from "../../assets/github.png";
import google from "../../assets/google.png";
import facebook from "../../assets/facebook.png";
import image from "../../assets/image.png";

export const Signup = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);


    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    const refreshToken = useRef(async () => {
        const refreshToken = localStorage.getItem('refreshToken');

        try {
            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            });

            if (!response.ok) {
                throw new Error('Error: ' + response.statusText);
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            if (data.refresh_token) {
                localStorage.setItem('refreshToken', data.refresh_token);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const decodedToken = jwtDecode(token);
                const expiresIn = decodedToken.exp * 1000 - new Date().getTime();
                setTimeout(refreshToken, expiresIn - 60000);
            } catch (error) {
                console.error("Invalid token", error);
            }
        }
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setErrorMessage('');
        setIsLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                }),
            });
            const data = await response.json();

            if (!response.ok) {
                const message = data?.error || 'Invalid email or password';
                setErrorMessage(message);
                setIsLoading(false);
                return;
            }

            
            if (data.access_token) {
                // Saves the access token into the browser’s localStorage so the user stays logged in.
                localStorage.setItem('token', data.access_token);
                // used to get new access token later
                localStorage.setItem('refreshToken', data.refresh_token);
                
                navigate('/overview')
                
            } else {
                setErrorMessage('Access token is missing in the response');
            }
        } catch (error) {
            console.error('Error:', error);
            setErrorMessage('Something went wrong. Please try again.');
        }
        setIsLoading(false); 
    };

    return (
       <div className="min-h-screen flex items-center justify-center bg-[#FFD1B0] px-4">
      <div className="w-full max-w-5xl bg-[#FEDCC5] rounded-3xl shadow-lg grid grid-cols-1 md:grid-cols-2 overflow-hidden">
        
        {/* Left side - Login form */}
        <div className="  bg:mx-20  bg:my-10 md:mx-10 md:my-10 rounded-2xl flex flex-col justify-center p-10 bg-opacity-50 bg-[rgba(255,242,233,0.5)] shadow-md">
          {/* Logo */}
          <img className='self-center mb-2 w-24 md:w-16' src={logo} alt="Logo" />
          <h2 className="self-center text-2xl mb-4">Sign Up</h2>

        
            {errorMessage && (
                    <div className="text-red-600 text-[10px] mt-2 text-center">{errorMessage}</div>
                )}
                 {isLoading && (
                    <div className="flex justify-center mt-2">
                            <div className="w-4 h-4 border-2 border-orange-500 border-dashed rounded-full animate-spin"></div>
                        </div>
                    // <div className="text-secondary text-xs text-[10px] mt-2 text-center">"Signing in... "</div>
                )}


          {/* Form */}
          <form className="space-y-2" onSubmit={handleSubmit}>
            <div>
              <label className="block text-[10px] mb-1">Name</label>
               <input
                        className="w-full p-2 text-[10px] bg-white rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
                        type="name"
                        placeholder="Name"
                        value={name}
                        onChange={e => setName(e.target.value)}
                    />
            </div>
            <div>
              <label className="block text-[10px] mb-1">Email</label>
               <input
                        className="w-full p-2 text-[10px] bg-white rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
            </div>
              <label className="block text-[10px] mb-2">Password</label>

            <div className='relative   rounded-[8px]'>
              <input
                        className="w-full p-2  text-[10px] bg-white rounded-md  focus:outline-none focus:ring-2 focus:ring-orange-400"
                            type={passwordVisible ? "text" : "password"}
                            placeholder="Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                        <div className='absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5'>
                            {passwordVisible ? (
                                <PiEyeLight className='fill-Heading' onClick={togglePasswordVisibility} />
                            ) : (
                                <PiEyeSlash className='fill-Heading' onClick={togglePasswordVisibility} />
                            )}
                        </div>
                    </div>
                    <div className='flex items-center justify-between'>
                        <div className='flex  items-center space-x-2 font-body text-[10px] font-normal text-Heading'>
                            <input type='checkbox' />
                            <label>Remember me</label>
                        </div>
                        <p className="text-right mt-2 text-[10px] text-orange-500 cursor-pointer hover:underline">
                            Forgot Password?
                        </p>
                    </div>

            <button
              type="submit"
              className="w-full bg-[#F25019] text-[10px] text-semibold text-white py-2 rounded-xl hover:bg-orange-600 transition"
            >
              Create Account
            </button>
          </form>

          {/* Divider */}
          <div className="my-3 flex items-center">
            <div className="flex-1 border-t border-gray-300"></div>
            <span className="px-3 text-[10px] text-gray-500">Or Continue With</span>
            <div className="flex-1 border-t border-gray-300"></div>
          </div>

           {/* Social login */}
          <div className="flex justify-center gap-4">
            <button className=" p-2 w-full flex items-center justify-center rounded-full bg-white hover:bg-gray-100">
              <img src={google} alt="Google" className="w-6 h-6 " />
            </button>
            {/* <button className="p-3 rounded-full  bg-white hover:bg-gray-100">
              <img src={github} alt="GitHub" className="w-6 h-6" />
            </button>
            <button className="p-3 rounded-full bg-white  hover:bg-gray-100">
              <img src={facebook} alt="Facebook" className="w-6 h-6" />
            </button> */}
          </div> 
          <p className="mt-6 text-center text-[10px]">
            Aready have an account?{" "}
            <span className="text-orange-600 font-medium cursor-pointer hover:underline" onClick={()=> navigate('/signin')} >
              Login
            </span>
          </p>

          {/* Register link */}
        
        </div>

        {/* Right side - Illustration (hidden on small screens) */}
        <div className="hidden md:flex items-center justify-center bg-[FEDCC5]">
          <img
            src={image}
            alt="Illustration"
            className="max-w-sm"
          />
        </div>
      </div>
    </div> 
    );
}





