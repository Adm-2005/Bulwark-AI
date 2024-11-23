import { Link } from "react-router-dom";
import { IconContext } from "react-icons/lib";
import { GiBorderedShield } from "react-icons/gi";
import { CiMenuKebab } from "react-icons/ci";
import { navLinks } from "../utils";

const Navbar = () => {
    return (
        <nav className="bg-gradient-to-r from-[#142462] to-[#030A10] w-full p-7 flex items-center justify-around">
            <Link to="/">
                <div className="flex gap-1 text-white text-2xl items-center font-poppins font-bold">
                    <IconContext.Provider value={{ size: '35px', color: '#FFAE52' }}>
                        <GiBorderedShield />
                    </IconContext.Provider>
                    Bulwark <span className="text-[#E3436B]">AI</span>
                </div>
            </Link>

            <ul className="flex lg:flex-row gap-8">
                {navLinks.map((navLink, index) => (
                    <Link key={index} to={navLink.link}>
                        <li className="text-md text-gray-300 hover:text-gray-500 font-poppins">{navLink.name}</li>
                    </Link>
                ))}
            </ul>

            <Link to="/sign-in">
                <button className="bg-gradient-to-r from-[#ffae52] to-[#E3436B] hover:bg-[#E3436B] cursor-pointer text-lg text-white font-poppins font-medium py-[8px] px-[18px] rounded-full shadow-xl">
                    Sign In
                </button>
            </Link>
        </nav>
    )
}

export default Navbar;