import { Col, Divider, List, Row } from "antd"
import "./styles.css"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { TeaserData } from "../../lib/types"

export const Settings = () => {

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ teasers, setTeasers ] = useState<Array<string>>( [] )

  const fetcTeasers = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getTeaserListsUrl() )
    const teaserData: TeaserData = await response.json();
    setTeasers( teaserData.teasers )
    setLoading( false )
  }

  useEffect( () => {
    fetcTeasers()
  }, [] )

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
        dataSource={ teasers }
        renderItem={ ( item ) => <List.Item>{ item }</List.Item> }
      />
    </>
  )
}