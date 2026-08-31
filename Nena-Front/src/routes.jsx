import { Layout } from "./Components/Layout/Layout";
import { SideBar } from "./Components/SideBar/SideBar"
import { Feedback } from  "./pages/feedback/Feedback"
import{ Overview} from "./pages/overview/Overview";
import {Recording} from "./pages/recording/Recording";
import {Profile} from "./pages/profile/Profile";
import { Signup } from "./pages/signup/Signup";
import { Login } from "./pages/login/Login";
import { Vocab } from "./pages/vocab/Vocab";
import { Practice } from "./pages/practice/Practice";

const routes = [
    {
        path: "/signin",
        Element: Login,
        isAuthenticated: false,
        layout: "None",
        Sidebar: null,
    },
    {
        path: "/signup",
        Element: Signup,
        isAuthenticated: false,
        layout: "None",
        Sidebar: null,
    },
    {
        path: "/overview",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Overview />
            </Layout>
        ),
        isAuthenticated: false,
    },
    {
        path: "/feedback",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Feedback/>
            </Layout>
        ),
        isAuthenticated: true,
    },
    {
        path: "/recording",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Recording />
            </Layout>
        ),
        isAuthenticated: true,
    },
    {
        path: "/practice/:modeSlug",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Practice />
            </Layout>
        ),
        isAuthenticated: false,
    },
    {
        path: "/profile",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Profile/>
            </Layout>
        ),
        isAuthenticated: true,
    },
     {    path: "/vocab",
        Element: () => (
            <Layout Sidebar={SideBar}>
                <Vocab/>
            </Layout>
        ),
        isAuthenticated: true,
    },
];

export default routes;