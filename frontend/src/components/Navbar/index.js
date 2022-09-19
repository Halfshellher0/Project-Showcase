import React from 'react';
import {FaBars, FaUnlock} from 'react-icons/fa';
import {
  Nav,
  NavbarContainer,
  NavLogo,
  MobileIcon,
  NavMenu,
  NavItem,
  NavLinks,
  NavBtn,
  NavBtnLink
} from './NavbarElements';

const Navbar = () => {
  return (
    <>
      <Nav>
        <NavbarContainer>
          <NavLogo to="/">Matt Turinski</NavLogo>
          <MobileIcon>
             <FaBars />
          </MobileIcon>
          <NavMenu>
            <NavItem>
              <NavLinks to="profile">Profile</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="experience">Experience</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="projects">Projects</NavLinks>
            </NavItem>
            <NavItem>
              <NavLinks to="experience">Contact</NavLinks>
            </NavItem>
          </NavMenu>
          <NavBtn>
            <NavBtnLink to="/unlock"><FaUnlock/></NavBtnLink>
          </NavBtn>
        </NavbarContainer>
      </Nav>
    </>
  )
}

export default Navbar;