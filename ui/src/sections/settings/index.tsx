import { Button, Col, Divider, Input, List, Row, Skeleton, Table } from "antd"
import "./styles.css"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { LikesData, SettingsData, SettingsOtherData } from "../../lib/types"
import { ApiOutlined, KeyOutlined, SaveOutlined } from "@ant-design/icons"

interface Props {
  errorMessage: ( message: string ) => void
  successMessage: ( message: string ) => void
}

export const Settings = ( {
  errorMessage,
  successMessage
}: Props ) => {

  const rowGutter = { xs: 8, sm: 16, md: 24, lg: 32 }

  const [ apiKey, setApiKey ] = useState<string>()
  const [ apiLoading, setApiLoading ] = useState<boolean>( false )
  const [ baseUrl, setBaseUrl ] = useState<string>()
  const [ likesLoading, setLikesLoading ] = useState<boolean>( false )
  const [ settings, setSettings ] = useState<SettingsData>()
  const [ otherSettings, setOtherSettings ] = useState<Array<SettingsOtherData>>( [] )
  const [ settingsLoading, setSettingsLoading ] = useState<boolean>( false )
  const [ urlLoading, setUrlLoading ] = useState<boolean>( false )

  const otherSettingsColumns = [
    {
      title: 'Name',
      dataIndex: 'description',
      key: 'name',
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
    },
    {
      title: 'Additional',
      dataIndex: 'additionalDescription',
      key: 'additional',
    },
    {
      title: 'Additional value',
      dataIndex: 'additionalValue',
      key: 'avalue',
    },
  ]

  const fetchSettings = async () => {
    setSettingsLoading( true )
    const response = await fetch( UrlUtility.getSettingsUrl() )
    const settingsData: SettingsData = await response.json();
    setSettings( settingsData )
    setOtherSettings( [ {
      description: 'Scheduled users',
      key: 1,
      value: settingsData.scheduled === undefined ? 0 : settingsData.scheduled,
    } ] )
    setSettingsLoading( false )
  }

  const fetcLikes = async () => {
    setLikesLoading( true )
    const response = await fetch( UrlUtility.getSettingsLikesUrl() )
    const likesData: LikesData = await response.json()
    setOtherSettings( ( current: Array<SettingsOtherData> ) => current.concat( {
      additionalDescription: "Until",
      additionalValue: likesData.rate_limited_until,
      description: "Remaining likes",
      key: 2,
      value: likesData.likes_remaining,
    } ) )
    setLikesLoading( false )
  }

  const updateApiKey = async () => {
    if ( apiKey !== undefined ) {
      setApiLoading( true )
      const response = await fetch( UrlUtility.getSettingsUpdateApiKeyUrl( apiKey ), { method: "POST" } )
      if ( response.status == 200 ) {
        successMessage( "API key updated" )
        setApiKey( undefined )
      } else {
        errorMessage( "Failed to update API key" )
      }
      setApiLoading( false )
    }
  }

  const updateBaseUrl = async () => {
    if ( baseUrl !== undefined ) {
      setUrlLoading( true )
      const response = await fetch( UrlUtility.getSettingsBaseUrl( baseUrl ), { method: "POST" } )
      if ( response.status == 200 ) {
        successMessage( "Base URL updated" )
      } else {
        errorMessage( "Failed to update Base URL" )
      }
      setUrlLoading( false )
    }
  }

  const getMaskedApiKey = () => {
    if (settings !== undefined && settings.apiKey !== undefined) {
      return new Array( settings.apiKey.length ).join( "*" )
    }
    return ""
  }

  const Teasers = () => settingsLoading ? (
    <Skeleton loading active>
      <List.Item.Meta avatar={ <Skeleton.Image /> } />
    </Skeleton>
  ) : (
    <List
      size="large"
      bordered
      dataSource={ settings?.teasers }
      renderItem={ ( item ) => <List.Item>{ item }</List.Item> }
    />
  )

  const OtherSettings = () => likesLoading || settingsLoading ? (
    <Skeleton loading active>
      <List.Item.Meta avatar={ <Skeleton.Image /> } />
    </Skeleton>
  ) : (
    <Table columns={ otherSettingsColumns } dataSource={ otherSettings } pagination={ false } />
  )

  useEffect( () => {
    fetchSettings()
    fetcLikes()
  }, [] )

  return (
    <>
      <Divider className="settings-divider" orientation="left">Settings</Divider>
      <Row className="settings-key" gutter={ rowGutter }>
        <Col className="gutter-row" xs={ 24 } sm={ 8 } md={ 6 } xl={ 4 }>
          Add / Update API key
        </Col>
        <Col className="gutter-row" xs={ 24 } sm={ 16 } md={ 18 } xl={ 20 }>
          <Input
            addonBefore={ <KeyOutlined /> }
            addonAfter={ (
              <Button
                className="addon-button"
                loading={ apiLoading }
                onClick={ updateApiKey }>
                <SaveOutlined />
              </Button>
            ) }
            onChange={ ( event: any ) => setApiKey( event.target.value ) }
            placeholder={ getMaskedApiKey() }
            value={ apiKey } />
        </Col>
      </Row>
      <Row className="settings-url" gutter={ rowGutter }>
        <Col className="gutter-row" xs={ 24 } sm={ 8 } md={ 6 } xl={ 4 }>
          Add / Update base URL
        </Col>
        <Col className="gutter-row" xs={ 24 } sm={ 16 } md={ 18 } xl={ 20 }>
          <Input
            addonBefore={ <ApiOutlined /> }
            addonAfter={ (
              <Button
                className="addon-button"
                loading={ urlLoading }
                onClick={ updateBaseUrl }>
                <SaveOutlined />
              </Button>
            ) }
            onChange={ ( event: any ) => setBaseUrl( event.target.value ) }
            placeholder={ settings?.baseUrl }
            value={ baseUrl } />
        </Col>
      </Row>
      <Divider className="settings-divider" orientation="left">Teaser likes</Divider>
      <Teasers />
      <Divider className="settings-divider" orientation="left">Other data</Divider>
      <OtherSettings />
    </>
  )
}