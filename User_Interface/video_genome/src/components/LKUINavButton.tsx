import React from 'react'
import { useLocation, Link } from 'react-router-dom';

interface LKUINavButtonProps {
    path: string;
    regComponent: React.ComponentType;
    filledComponent: React.ComponentType
}
function LKUINavButton({ path, regComponent, filledComponent }: LKUINavButtonProps) {
    const loc = useLocation()
    const isDesignatedPage = loc.pathname === path
    const IconPath = isDesignatedPage ? filledComponent : regComponent
    return (
        <Link to={path} className="lkui-path-no-dec">
            <div className='lkui-nav-button'>
                <IconPath />
            </div>
        </Link>
    )
}
export default LKUINavButton