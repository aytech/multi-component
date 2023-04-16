import { useEffect, useRef, useState } from 'react'
import './styles.css'
import { Card, Carousel, Image, Layout, Menu, Space } from 'antd'
import { Content, Footer, Header } from 'antd/es/layout/layout'
import Meta from 'antd/es/card/Meta'

function App() {

  const dataFetchedRef = useRef( false )
  const [ profiles, setProfiles ] = useState<Array<any>>( [] )

  useEffect( () => {
    if ( dataFetchedRef.current !== true ) {
      dataFetchedRef.current = true
      console.log( "UseEffect called!" )
      fetch( 'http://localhost:5000/users?page=1' )
        .then( response => response.json() )
        .then( ( data: Array<any> ) => {
          setProfiles( data )
        } )
    }
  }, [] )

  return (
    <Layout>
      <Header style={ {
        position: 'sticky',
        top: 0,
        zIndex: 1,
        width: '100%'
      } }>
        <div style={ {
          float: 'left',
          width: 120,
          height: 31,
          margin: '16px 24px 16px 0',
          background: 'rgba(255, 255, 255, 0.2)'
        } } />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={ [ '2' ] }
          items={ new Array( 3 ).fill( null ).map( ( _, index ) => ( {
            key: String( index + 1 ),
            label: `nav ${ index + 1 }`,
          } ) ) } />
      </Header>
      <Content style={ { padding: "20px" } }>
        <Space direction='horizontal' style={ { marginBottom: "20px" } }>
          { profiles.slice( 0, 5 ).map( profile =>
            <Card
              hoverable
              style={ { height: 470, width: 240 } }
              cover={
                <Carousel autoplay dots={ { className: "photo-dots" } }>
                  { profile.photos.map( ( photo: any ) => (
                    <Image
                      width={ 240 }
                      src={ photo.url }
                      placeholder={
                        <Image
                          preview={ false }
                          src={ `${ photo.url }?x-oss-process=image/blur,r_50,s_50/quality,q_1/resize,m_mfit,h_200,w_200` }
                          width={ 240 } /> } />
                  ) ) }
                </Carousel>
              }>
              <Meta title={ profile.name } description="Not fetched yet"></Meta>
            </Card>
          ) }
        </Space>
        <Space direction='horizontal' style={ { marginBottom: "20px" } }>
          { profiles.slice( 5 ).map( profile =>
            <Card
              hoverable
              style={ { height: 420, width: 240 } }
              cover={
                <Carousel dots={ { className: "photo-dots" } }>
                  { profile.photos.map( ( photo: any ) => (
                    <Image
                      width={ 240 }
                      src={ photo.url }
                      placeholder={
                        <Image
                          preview={ false }
                          src={ `${ photo.url }?x-oss-process=image/blur,r_50,s_50/quality,q_1/resize,m_mfit,h_200,w_200` }
                          width={ 240 } /> } />
                  ) ) }
                </Carousel>
                // <img alt="card" src={ profile.photos.length > 0 ? profile.photos[ 0 ].url : 'https://place-hold.it/240' } /> 
              }>
              <Meta title={ profile.name } description="Not fetched yet"></Meta>
            </Card>
          ) }
        </Space>
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
