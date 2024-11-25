import { Link } from "react-router-dom";
import { IconContext } from "react-icons/lib";
import { GiNetworkBars } from "react-icons/gi";
import { CiMenuKebab } from "react-icons/ci";

const NetworkCard = ({ network, color }) => {

    return (
        <div className={`flex relative p-3 w-[700px] border border-${color} justify-between items-center rounded-lg`}>
            <div className={`flex items-center justify-center p-4 h-full rounded-full bg-${color} absolute -left-6`}>
                <IconContext.Provider value={{ size:'35px', color: 'white' }}>
                    <GiNetworkBars />
                </IconContext.Provider>
            </div>

            <h3 className="text-white text-lg font-poppins ml-10">{network.name}</h3>
            
            <div className="flex">
                <Link to="/dashboard">
                    <button
                        className={`py-[8px] px-[18px] bg-${color} text-white rounded-lg`}
                    >
                        View Logs
                    </button>
                </Link>
                
                <IconContext.Provider value={{ size: '35px', color:'white' }}>
                    <CiMenuKebab />
                </IconContext.Provider>
            </div>
        </div>
    )
}

export default NetworkCard;