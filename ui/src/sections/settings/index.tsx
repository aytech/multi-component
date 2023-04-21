import { Col, Divider, List, Row } from "antd"
import "./styles.css"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"

export const Settings = () => {

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ teaserList, setTeaserList ] = useState<Array<string>>( [] )

  const fetcTeaserList = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getTeaserListsUrl() )
    const teaserData: Array<string> = await response.json();
    setTeaserList( teaserData )
    setLoading( false )
  }

  useEffect( () => {
    fetcTeaserList()
  } )

  return (
    <>
      <Divider className="settings-divider" orientation="left">API key</Divider>
      <Row gutter={ {
        xs: 8,
        sm: 16,
        md: 24,
        lg: 32,
      } }>
        <Col className="gutter-row" span={ 6 }>Add / Update API key</Col>
        <Col className="gutter-row" span={ 6 }>Input here</Col>
      </Row>
      <Divider className="settings-divider" orientation="left">Teaser likes</Divider>
      <List
        size="large"
        bordered
        dataSource={ teaserList }
        renderItem={ ( item ) => <List.Item>{ item }</List.Item> }
      />
    </>
  )
}