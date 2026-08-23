import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import routes from './routes';
import { Login } from './pages/login/Login';
import { Signup } from './pages/signup/Signup';
import AuthWrapper from './AuthWraper';
import { ToastContainer } from 'react-toastify';
import { useTheme } from './useTheme';

function App() {
  const { resolved } = useTheme();

  return (
    <Router       
      basename={import.meta.env.DEV ? '/' : '/nena-Front/'}
    >
      <Routes>


        <Route path="/signin" element={<Login />} /> 
        <Route path="/signup" element={<Signup />} /> 
        <Route path="/" element={<Navigate to="/signin" />} />

        
        {routes.map((route, index) => (
          (route.path !== "/signin" && route.path !== "/signup") &&
          <Route key={index} path={route.path} element={
            <AuthWrapper Sidebar={route.Sidebar}>
              <route.Element />
            </AuthWrapper>
            
          }/>
        ))}
       

      </Routes>
       <ToastContainer position="top-center" autoClose={3000} theme={resolved} />
    </Router>
  );
}


export default App
