import './styles.css'
import { Layout, message, theme } from 'antd'
import { Content } from 'antd/es/layout/layout'
import { AppHeader } from '../header'
import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AppSider } from '../sider'
import { Profiles } from '../profiles'
import { Settings } from '../settings'
import { Logs } from '../logs'

export const App = () => {

  const [ messageApi, contextHolder ] = message.useMessage();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const [ menuCollapsed, setMenuCollapsed ] = useState<boolean>( false );

  const errorMessage = ( message: string ) => {
    messageApi.open( {
      type: "error",
      content: message,
    } )
  }

  const successMessage = ( message: string ) => {
    messageApi.open( {
      type: "success",
      content: message,
    } )
  }

  return (
    <Layout>
      { contextHolder }
      <Router>
        <AppSider menuCollapsed={ menuCollapsed } />
        <Layout>
          <AppHeader colorBgContainer={ colorBgContainer } menuCollapsed={ menuCollapsed } setMenuCollapsed={ setMenuCollapsed } />
          <Content className="app-content">
            <Routes>
              <Route path="/" element={ <Profiles errorMessage={ errorMessage } successMessage={ successMessage } /> } />
              <Route path="/logs" element={ <Logs /> } />
              <Route path="/settings" element={ <Settings /> } />
            </Routes>
          </Content>
        </Layout>
      </Router>
    </Layout>
  )
}

export default App
