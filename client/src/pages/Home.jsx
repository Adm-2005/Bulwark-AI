import Navbar from '../components/Navbar';
import Hero from '../sections/Hero';
import Features from '../sections/Features';
import Footer from '../components/Footer';

const Home = () => {
    return (
        <div className="bg-gradient-to-r from-[#142462] to-[#030A10] w-full flex flex-col min-h-screen">
            <Navbar />

            <Hero />

            <Features />

            <Footer />
        </div>
    )
}

export default Home;