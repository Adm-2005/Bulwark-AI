import Navbar from '../components/Navbar';
import BarChart from '../components/BarChart';
import LineChart from '../components/LineChart';
import Footer from '../components/Footer';
import { mockLogs } from '../utils';

const Dashboard = () => {
    return (
        <div className="bg-gradient-to-r from-[#142462] to-[#030A10] w-full flex flex-col gap-7 min-h-screen">
            <Navbar />

            <h1 className='font-poppins text-3xl text-gray-400 text-center'>Log Analytics Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 mx-auto gap-6">
                <div className="p-5 bg-white/20 rounded shadow">
                  <h2 className="text-lg text-white text-center font-semibold font-poppins mb-3">Log Severity Distribution</h2>
                  <BarChart logs={mockLogs} />
                </div>
                <div className="p-5 bg-white/20 rounded shadow">
                  <h2 className="text-lg text-white text-center font-semibold font-poppins mb-3">Logs Over Time</h2>
                  <LineChart logs={mockLogs} />
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default Dashboard;