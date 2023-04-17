import { Card, Carousel, Col, Image, Row } from "antd"
import "./styles.css"
import { useEffect, useRef } from "react"
import { UsersData } from "../../lib/types"

interface Props {
  fetchUserData: () => void
  userData: UsersData | null
}

export const Gallery = ( {
  fetchUserData,
  userData
}: Props ) => {

  const { Meta } = Card
  const dataFetchedRef = useRef( false )

  useEffect( () => {
    if ( dataFetchedRef.current !== true ) {
      dataFetchedRef.current = true
      fetchUserData()
    }
  }, [ fetchUserData ] )

  const GalleryCollection = () => userData !== null ? (
    <>
      { userData.users.map( profile => (
        <Col
          className="card-col"
          key={ profile.s_number }>
          <Card
            className="profile-card"
            hoverable
            cover={
              <Carousel autoplay dots={ { className: "photo-dots" } }>
                { profile.photos.map( ( photo: any ) => (
                  <Image
                    key={ photo.photo_id }
                    width={ 240 }
                    src={ photo.url } />
                ) ) }
              </Carousel>
            }>
            <Meta title={ profile.name } description="Not fetched yet"></Meta>
          </Card>
        </Col>
      ) ) }
    </>
  ) : null

  return (
    <Row gutter={ 16 }>
      <GalleryCollection />
    </Row>
  )
}