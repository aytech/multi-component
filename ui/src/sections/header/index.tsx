import { MenuFoldOutlined, MenuUnfoldOutlined } from '@ant-design/icons'
import { Button, Layout } from 'antd'

interface Props {
  colorBgContainer: string
  menuCollapsed: boolean
  setMenuCollapsed: ( collapsed: boolean ) => void
}

export const AppHeader = ( {
  colorBgContainer,
  menuCollapsed,
  setMenuCollapsed
}: Props ) => {

  const { Header } = Layout

  return (
    <Header
      style={ {
        padding: 0,
        background: colorBgContainer,
      } }>
      <Button
        type="text"
        icon={ menuCollapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined /> }
        onClick={ () => setMenuCollapsed( !menuCollapsed ) }
        style={ {
          fontSize: '16px',
          width: 64,
          height: 64,
        } }
      />
    </Header>
  )
}