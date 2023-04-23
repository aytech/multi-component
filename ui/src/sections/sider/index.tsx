import { SettingOutlined, SnippetsOutlined, UserOutlined } from "@ant-design/icons"
import { Menu } from "antd"
import Sider from "antd/es/layout/Sider"
import { useLocation, useNavigate, useSearchParams } from "react-router-dom"
import "./styles.css"
import { useEffect, useState } from "react"

interface Props {
  menuCollapsed: boolean
}

export const AppSider = ( { menuCollapsed }: Props ) => {

  const location = useLocation()
  const navigate = useNavigate()

  const [ searchParams ] = useSearchParams()

  const [ selectedKeys, setSelectedKeys ] = useState<string[]>( [ "1" ] )

  useEffect( () => {
    switch ( location.pathname ) {
      case "/logs":
        setSelectedKeys( [ "2" ] )
        break
      case "/settings":
        setSelectedKeys( [ "3" ] )
        break
      default:
        setSelectedKeys( [ "1" ] )
    }

  }, [ location ] )

  return (
    <Sider trigger={ null } collapsible collapsed={ menuCollapsed }>
      <div className="logo" />
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={ selectedKeys }
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