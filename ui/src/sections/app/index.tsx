import { useEffect, useRef, useState } from 'react'
import './styles.css'
import { Card, Carousel, Col, Image, Layout, Menu, Row } from 'antd'
import { Content, Footer, Header } from 'antd/es/layout/layout'
import Meta from 'antd/es/card/Meta'

function App() {

  const dataFetchedRef = useRef( false )
  const [ profiles, setProfiles ] = useState<Array<any>>( [] )

  useEffect( () => {
    if ( dataFetchedRef.current !== true ) {
      dataFetchedRef.current = true
      console.log( "UseEffect called!" )
      fetch( '/api/users?page=1' )
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
        <Row gutter={ 16 }>
          { profiles.map( profile => (
            <Col className="card-col">
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
            </Col>
          ) ) }
        </Row>
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
