import React, { useEffect, useRef, useState } from "react";
import { Details } from "./Details";
import { jwtDecode } from "jwt-decode";
import toast from "react-hot-toast";

export const Profile = () => {
   const [user, setUser] = useState({});
  const [showNameModal, setShowNameModal] = useState(false);
  const [userNameData, setUsernameData] = useState({ username: "" });
  const [showContactModal, setShowContactModal] = useState(false);
  const [contact, setContact] = useState({ contact: "" });
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [email, setEmail] = useState({ email: "" });
  const [showImageModal, setShowImageModal] = useState(false);
  const [image, setImage] = useState({ image: "" });
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [password, setPassword] = useState({
    current: "",
    newpassword: "",
    confirmpassword: "",
  });
  const [preview, setPreview] = useState(null);
  const imageInputRef = useRef();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub;
    // console.log(token)
    // console.log(decodedToken)
    // console.log(userId)

    fetch(`http://127.0.0.1:5000/userById/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((resp) => resp.json())
      .then((data) => {
        setUser(data);
        console.log(data)
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage((prevFormData) => ({ ...prevFormData, image: file }));

    setPreview(URL.createObjectURL(file));
  };

  const handleUsernameChange = (e) => {
    const { id, value } = e.target;
    setUsernameData((userNameData) => ({ ...userNameData, [id]: value }));
  };

  const handlePasswordChange = (e) => {
    const { id, value } = e.target;
    setPassword((passwordData) => ({ ...passwordData, [id]: value }));
  };

  const handleContactChange = (e) => {
    const { id, value } = e.target;
    setContact((userNameData) => ({ ...userNameData, [id]: value }));
  };

  const handleEmailChange = (e) => {
    const { id, value } = e.target;
    setEmail((emailData) => ({ ...emailData, [id]: value }));
  };
const handleSubmitUsername = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    const userData = new FormData();
    userData.append("username", userNameData.username);

    fetch(`http://127.0.0.1:5000/userById/${userId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: userData,
    })
      .then((response) => response.json())
      .then((data) => {
        setUser(data);
        setShowNameModal(false);
        setUsernameData({ username: "" });
        toast.success("Username successfully Changed");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSubmitContact = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    const userData = new FormData();
    userData.append("contact", contact.contact);

    fetch(`http://127.0.0.1:5000/userById/${userId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: userData,
    })
      .then((response) => response.json())
      .then((data) => {
        setUser(data);
        setShowContactModal(false);
        setContact({ contact: "" });
        toast.success("Contact successfully Changed");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
    const handleSubmitEmail = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    const userData = new FormData();
    userData.append("email", email.email);

    fetch(`http://127.0.0.1:5000/userById/${userId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: userData,
    })
      .then((response) => response.json())
      .then((data) => {
        setUser(data);
        setShowEmailModal(false);
        setEmail({ email: "" });
        toast.success("Email successfully Changed");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSubmitImage = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    const userData = new FormData();
    userData.append("image", image.image);

    fetch(`http://127.0.0.1:5000/userById/${userId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: userData,
    })
      .then((response) => response.json())
      .then((data) => {
        setUser(data);
        setShowImageModal(false);
        setImage({ email: "" });
        toast.success("New image successfully uploaded");
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSubmitPassword = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.sub.id;

    if (
      password.newpassword == password.confirmpassword &&
      password.newpassword !== ""
    ) {
      const userData = new FormData();
      userData.append("newpassword", password.newpassword);

      fetch(`http://127.0.0.1:5000/userById/${userId}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
        },

        body: userData,
      })
        .then((response) => response.json())
        .then((data) => {
          setUser(data);
          setShowPasswordModal(false);
          setPassword({ password: "" });
          toast.success("Password successfully changed");
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      toast.error("Confirmed password does not match");
    }
  };

  let content;

  if (showNameModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-white dark:bg-variant1-dark p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-2xl  text-center text-Heading dark:text-primary-light">
            Change Name
          </h2>
          <form onSubmit={handleSubmitUsername}>
            <textarea
              id="username"
              value={userNameData.username}
              onChange={handleUsernameChange}
              className="w-full mb-2 p-2 border border-none rounded focus:outline-none bg-gray-200 rounded-lg"
            ></textarea>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                                onClick={() => setShowNameModal(false)}
                className="bg-gray-200 px-4 py-2 rounded hover:cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className=" bg-[#F25019] text-white px-4 py-2 rounded hover:cursor-pointer"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showContactModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-white dark:bg-variant1-dark p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-2xl  text-center text-Heading dark:text-primary-light">
            Change Contact
          </h2>
          <form onSubmit={handleSubmitContact}>
            <textarea
              id="contact"
              value={contact.contact}
              onChange={handleContactChange}
              className="w-full mb-2 p-2 border dark:border-none rounded focus:outline-none bg-gray-200 rounded-lg dark:bg-primary-dark text-Heading dark:text-primary-light "
            ></textarea>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowContactModal(false)}
                className="bg-gray-200 px-4 py-2 rounded hover:cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className=" bg-[#F25019] text-white px-4 py-2 rounded hover:cursor-pointer"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showEmailModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-white dark:bg-variant1-dark p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-2xl  text-center text-Heading dark:text-primary-light">
            Change Email
          </h2>
          <form onSubmit={handleSubmitEmail}>
            <textarea
              id="email"
              value={email.email}
              onChange={handleEmailChange}
              className="w-full mb-2 p-2 border dark:border-none rounded focus:outline-none bg-gray-200 rounded-lg dark:bg-primary-dark text-Heading dark:text-primary-light "
            ></textarea>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowEmailModal(false)}
                className="bg-gray-200 px-4 py-2 rounded hover:cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className=" bg-[#F25019] text-white px-4 py-2 rounded hover:cursor-pointer"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showImageModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-white dark:bg-variant1-dark p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-2xl  text-center text-Heading dark:text-primary-light">
            Change image
          </h2>
          <form onSubmit={handleSubmitImage}>
            <input
              ref={imageInputRef}
              id="image"
              type="file"
              name="image"
              onChange={handleImageChange}
              className="w-full px-4 py-2 bg-Primary rounded-md text-sm mb-3  bg-gray-200 rounded-lg text-Variant2 outline-none"
            />
            {preview && (
              <img
                src={preview}
                alt="Preview"
                className="w-full h-64 object-cover mt-4"
              />
            )}

            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowImageModal(false)}
                className="bg-gray-200 px-4 py-2 rounded hover:cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                               className=" bg-[#F25019] text-white px-4 py-2 rounded hover:cursor-pointer"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else if (showPasswordModal) {
    content = (
      <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
        <div className="bg-white dark:bg-variant1-dark p-4 rounded shadow-lg max-w-full w-[350px] lg:w-[500px]">
          <h2 className="mb-2 text-2xl  text-center text-Heading dark:text-primary-light">
            Change Password
          </h2>
          <form onSubmit={handleSubmitPassword}>
            <label htmlFor="">
              Current Password
              <input
                id="current"
                value={password.current}
                onChange={handlePasswordChange}
                className="w-full mb-2 p-2 border dark:border-none rounded focus:outline-none bg-gray-200 rounded-lg dark:bg-primary-dark text-Heading dark:text-primary-light "
              ></input>
            </label>
            <label htmlFor="">
              New Password
              <input
                id="newpassword"
                value={password.newpassword}
                onChange={handlePasswordChange}
                className="w-full mb-2 p-2 border dark:border-none rounded focus:outline-none bg-gray-200 rounded-lg dark:bg-primary-dark text-Heading dark:text-primary-light "
              ></input>
            </label>
            <label htmlFor="">
              Confirm Password
              <input
                id="confirmpassword"
                value={password.confirmpassword}
                onChange={handlePasswordChange}
                className="w-full mb-2 p-2 border dark:border-none rounded focus:outline-none bg-gray-200 rounded-lg dark:bg-primary-dark text-Heading dark:text-primary-light "
              ></input>
            </label>

            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowPasswordModal(false)}
                className="bg-gray-200 px-4 py-2 rounded hover:cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                 className=" bg-[#F25019]text-white px-4 py-2 rounded hover:cursor-pointer"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  } else {
    content = (
      <Details
        user={user}
        setShowNameModal={setShowNameModal}
        setShowPasswordModal={setShowPasswordModal}
        setShowImageModal={setShowImageModal}
        setShowEmailModal={setShowEmailModal}
        setShowContactModal={setShowContactModal}
      />
    );
  }

  return (
    <div className="h-screen ">
      <div className="">
        {/* heading */}
        <div className="text-xl font-semibold p-7 mb-7 font-body bg-[#FFEEE3] text-[#F25019]  ">Account</div>
        <div className="flex flex-wrap justify ">
          <div className=" lg:w-1/4 flex  lg:flex-col  items-center w-full justify-center ">
            <div className="pl-5  ">
              <div className="text-Secondary font-body text-center">
                Welcome!
              </div>
              <div className="text-center">{user.name}</div>
            </div>
            <div className="rounded-full  border lg:w-52 lg:h-52 mt-5  ml-3">
              <img
                className="rounded-full object-cover lg:h-52 lg:w-52 w-32 h-32 "
                src={user.image}
                alt=""
              />
            </div>
            
          </div>
          <div className="lg:w-3/4 mb-4 py-4 w-full ">{content}</div>
        </div>
      </div>
    </div>
  );
};