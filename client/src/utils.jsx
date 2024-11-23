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


const footerLinks = [

];

export { routes, navLinks, footerLinks };