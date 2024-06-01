import { Outlet, Link } from "react-router-dom";
import { Menu } from "antd";
import { HomeOutlined, TrophyOutlined } from "@ant-design/icons";

const Layout = () => {
  const menuItems = [
    {
      key: "1",
      label: (
        <Link to="/">Welcome</Link>
      )
    },
    {
      key: "2",
      label: (
        <Link to="/home">
          <HomeOutlined />
          <span style={{ marginLeft: "4px" }}>Home</span>
        </Link>
      )
    },
    {
      key: "3",
      label: (
        <Link to="/tournament">
          <TrophyOutlined />
          <span style={{ marginLeft: "4px" }}>Tournament</span>
        </Link>
      )
    }
  ];

  return (
    <>
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]} items={menuItems} />
      <Outlet />
    </>
  );
};

export default Layout;