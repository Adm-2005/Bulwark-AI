import Home from './pages/Home.jsx';
import Error from './pages/Error.jsx';
import Network from './pages/Network.jsx';
import SignUp from './pages/SignUp.jsx';
import SignIn from './pages/SignIn.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Profile from './pages/Profile.jsx';

const routes = [
    {
        path: '/',
        element: <Home />,
        errorElement: <Error />
    },
    {
        path: '/sign-in',
        element: <SignIn />,
    },
    {
        path: '/sign-up',
        element: <SignUp />,
    },
    {
        path: '/networks',
        element: <Network />
    },
    {
        path: '/dashboard',
        element: <Dashboard />
    }, 
    {
        path: '/profile/:id',
        element: <Profile />
    }
];

const navLinks = [
    {
        name: 'Home',
        link: '/'
    },
    {
        name: 'Networks',
        link: '/networks'
    },
    {
        name: 'Dashboard',
        link: '/dashboard'
    },
    {
        name: 'Profile',
        link: '/profile'
    },
    {
        name: 'Settings',
        link: '/settings'
    }
];

const mockLogs = [
    { timestamp: "2024-11-24T12:00:00Z", severity: "Info" },
    { timestamp: "2024-11-24T12:05:00Z", severity: "Error" },
    { timestamp: "2024-11-24T12:10:00Z", severity: "Critical" },
    { timestamp: "2024-11-24T12:15:00Z", severity: "Info" },
    { timestamp: "2024-11-24T12:20:00Z", severity: "Warn" },
    { timestamp: "2024-11-24T12:25:00Z", severity: "Error" },
    { timestamp: "2024-11-24T12:30:00Z", severity: "Critical" },
];

const footerLinks = [

];

export { routes, navLinks, footerLinks, mockLogs };