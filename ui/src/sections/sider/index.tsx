import { SettingOutlined, SnippetsOutlined, UserOutlined } from "@ant-design/icons"
import { Menu } from "antd"
import Sider from "antd/es/layout/Sider"
import { useNavigate, useSearchParams } from "react-router-dom"
import "./styles.css"

interface Props {
  menuCollapsed: boolean
}

export const AppSider = ( { menuCollapsed }: Props ) => {

  const navigate = useNavigate()

  const [ searchParams ] = useSearchParams()

  return (
    <Sider trigger={ null } collapsible collapsed={ menuCollapsed }>
      <div className="logo" />
      <Menu
        theme="dark"
        mode="inline"
        defaultSelectedKeys={ [ '1' ] }
        items={ [
          {
            key: "1",
            icon: <UserOutlined />,
            label: "Profiles",
            onClick: () => navigate( `/?${ searchParams.toString() }` )
          },
          {
            key: "2",
            icon: <SnippetsOutlined />,
            label: "Logs",
            onClick: () => navigate( "/logs" )
          },
          {
            key: "3",
            icon: <SettingOutlined />,
            label: "Settings",
            onClick: () => navigate( "/settings" )
          },
        ] }
      />
    </Sider>
  )
}