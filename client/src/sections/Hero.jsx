import { Link } from "react-router-dom";

const Hero = () => {
    return (
        <section id="" className="flex w-full items-center justify-around p-7">
            <div className="flex flex-col gap-2 w-1/2 pl-[140px]">
                <h1 className="text-4xl text-white font-poppins font-extrabold">Protect Networks, Detect Threats, Automate Responses</h1>
                <p className="text-md text-gray-200 font-poppins font-medium">Empower your network security with seamless anomaly detection, instant alerts, and automated remediation. Simplify operations and safeguard data with cutting-edge intelligence-driven solutions.</p>
                <div className="flex gap-3 mt-4">
                    <Link to="/sign-up">
                        <button className="text-white font-poppins bg-gradient-to-r from-primary to-[#455ae6] shadow-sm shadow-primary py-[8px] px-[18px] rounded-full">
                            Get Started
                        </button>
                    </Link>
                    <Link to="/">
                        <button className="text-white font-poppins border border-white py-[8px] px-[18px] rounded-full">
                            Learn More
                        </button>
                    </Link>
                </div>
            </div>
            <div className="flex w-1/2 items-center justify-center">
                <img src="/hero2.png"></img>
            </div>
        </section>
    )
}

export default Hero;