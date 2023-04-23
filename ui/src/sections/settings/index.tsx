import { Col, Divider, List, Row } from "antd"
import "./styles.css"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { LikesData, TeaserData } from "../../lib/types"

export const Settings = () => {

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ teasers, setTeasers ] = useState<Array<string>>( [] )
  const [ likes, setLikes ] = useState<LikesData>()

  const fetcTeasers = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getTeaserListsUrl() )
    const teaserData: TeaserData = await response.json();
    setTeasers( teaserData.teasers )
    setLoading( false )
  }

  const fetcLikes = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getSettingsLikesUrl() )
    const likesData: LikesData = await response.json()
    setLikes( likesData )
    setLoading( false )
  }

  useEffect( () => {
    fetcTeasers()
    fetcLikes()
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
      <Divider className="settings-divider" orientation="left">Likes remaining</Divider>
      <List
        size="large"
        bordered
        dataSource={ [ { ...likes, key: 1 } ] }
        renderItem={ ( item ) => (
          <List.Item>
            <strong>Remaining:</strong> { item.likes_remaining }&nbsp;
            <strong>until:</strong> { item.rate_limited_until }
          </List.Item>
        ) }
      />
    </>
  )
}