import { Layout } from 'antd'

export const AppHeader = () => {

  const { Header } = Layout

  return (
    <Header className="app-header">
      <div className="brand" />
      {/* <Menu
        theme="dark"
        mode="horizontal"
        defaultSelectedKeys={ [ '2' ] }
        items={ new Array( 3 ).fill( null ).map( ( _, index ) => ( {
          key: String( index + 1 ),
          label: `nav ${ index + 1 }`,
        } ) ) } /> */}
    </Header>
  )
}