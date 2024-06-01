import { Outlet, Link, useLocation } from "react-router-dom";
import { Menu } from "antd";
import { HomeOutlined, TrophyOutlined } from "@ant-design/icons";
import { useEffect, useState } from 'react';
import { useUser } from "../../UserContext";

const Layout = () => {
  const location = useLocation();
  const [userName] = useUser();
  
  const [selectedKey, setSelectedKey] = useState("1");

  useEffect(() => {
    setSelectedKey(menuItems.find(item => item.path === location.pathname)?.key || "1");
  }, [userName, location.pathname]);

  const menuItems = [
    {
      key: "1",
      label: (
        <Link to="/">Welcome</Link>
      ),
      path: "/",
      show: !userName 
    },
    {
      key: "2",
      label: (
        <Link to={`/home/${userName}`}>
          <HomeOutlined />
          <span style={{ marginLeft: "4px" }}>Home</span>
        </Link>
      ),
      path: userName ? `/home/${userName}` : "/home",
      show: !!userName 
    },
    {
      key: "3",
      label: (
        <Link to="/tournament">
          <TrophyOutlined />
          <span style={{ marginLeft: "4px" }}>Tournament</span>
        </Link>
      ),
      path: "/tournament",
      show: !!userName 
    }
  ];

  return (
    <>
      <Menu theme="dark" mode="horizontal" selectedKeys={[selectedKey]}>
        {menuItems.filter(item => item.show).map(item => (
          <Menu.Item key={item.key}>{item.label}</Menu.Item>
        ))}
      </Menu>
      <Outlet />
    </>
  );
};

export default Layout;
