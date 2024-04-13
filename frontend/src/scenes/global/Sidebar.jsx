import {  useState } from "react";
import { Sidebar, Menu, MenuItem } from "react-pro-sidebar";
import {Box, IconButton, Typography, useTheme} from "@mui/material";
import { Link } from "react-router-dom";
import {tokens} from "../../theme";
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import MeetingRoomOutlinedIcon from '@mui/icons-material/MeetingRoomOutlined';

//Still mssing -> hover color and nicer background color and backgroud color for selected item

const Item = ({ title, to, icon, selected, setSelected }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette);
    return (
      <MenuItem
        active={selected === title}
        style={{
          color: colors.grey[900],
        }}
        onClick={() => setSelected(title)}
        icon={icon}
      >
        <Typography>{title}</Typography>
        <Link to={to} />
      </MenuItem>
    );
  };

  
const FancySidebar = () => {

    const theme = useTheme();
    const colors = tokens(theme.palette)
    // state for menu collapse
    const [isCollapsed, setIsCollapsed] = useState(false);
    // state for current page
    const [selected, setSelected] = useState('Overview');

    return(
            <Sidebar collapsed={isCollapsed} backgroundColor={colors.blue[100]} breakPoint="md">
                <Menu iconShape="round">
                    <MenuItem
                        onClick={() => setIsCollapsed(!isCollapsed)}
                        icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
                        style={{
                        margin: "10px 0 20px 0",
                        color: colors.grey[900],
                        }}
                    >
                    {!isCollapsed && (
                        <Box
                            display="flex"
                            justifyContent="space-between"
                            alignItems="center"
                            textAlign="center"
                            ml="15px"
                        >
                            <Typography variant="h3" color={colors.grey[900]}>
                            Menu
                            </Typography>
                            <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                                <MenuOutlinedIcon style={{color: colors.grey[900],}} />
                            </IconButton>
                        </Box>
                        )}
                    </MenuItem>

                    <Box paddingLeft={isCollapsed ? undefined : "10%"}>
                        <Item
                            title="Dashboard"
                            to="/"
                            icon={<HomeOutlinedIcon />}
                            selected={selected}
                            setSelected={setSelected}
                        />
                        <Item
                            title="Lecture Hall 18"
                            to="/lh18"
                            icon={<MeetingRoomOutlinedIcon />}
                            selected={selected}
                            setSelected={setSelected}
                        />
                        <Item
                            icon={<MeetingRoomOutlinedIcon />}
                            title="Lecture Hall 19"
                            to="/lh19"
                            selected={selected}
                            setSelected={setSelected}
                        />
                    </Box>
                </Menu>
            </Sidebar>
    );
}
export default FancySidebar;