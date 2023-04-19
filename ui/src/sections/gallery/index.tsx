import { Card, Carousel, Col, Image, Row } from "antd"
import "./styles.css"
import { UsersData } from "../../lib/types"

interface Props {
  userData: UsersData | null
}

export const Gallery = ( {
  userData
}: Props ) => {

  const { Meta } = Card

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
              <Carousel dots={ { className: "photo-dots" } }>
                { profile.photos.map( ( photo: any ) => (
                  <Image
                    key={ photo.photo_id }
                    width={ 240 }
                    src={ photo.url }
                    style={ { overflow: 'hidden' } } />
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