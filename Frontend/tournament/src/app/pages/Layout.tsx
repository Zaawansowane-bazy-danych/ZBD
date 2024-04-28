import { Outlet, Link } from "react-router-dom";
import { Menu } from "antd";
import { HomeOutlined, TrophyOutlined } from "@ant-design/icons";

const Layout = () => {
  return (
    <>
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
        <Menu.Item key="1">
          <Link to="/">Welcome</Link>
        </Menu.Item>
        <Menu.Item key="2">
          <Link to="/home">
            <HomeOutlined />
            Home
          </Link>
        </Menu.Item>
        <Menu.Item key="3">
          <Link to="/tournament">
            <TrophyOutlined />
            Tournament
          </Link>
        </Menu.Item>
      </Menu>

      <Outlet />
    </>
  );
};

export default Layout;