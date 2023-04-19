import { Button, Card, Carousel, Col, Image, Row, Space } from "antd"
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import "./styles.css"
import { UsersData } from "../../lib/types"

interface Props {
  userData: UsersData | null
}

export const Gallery = ( {
  userData
}: Props ) => {

  const { Meta } = Card

  const LikedIcon = ( { liked }: { liked: boolean } ) => {
    return liked ? (
      <CheckCircleOutlined style={ { fontSize: "24px", color: "green" } } />
    ) : (
      <CloseCircleOutlined style={ { fontSize: "24px", color: "red" } } />
    )
  }

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
                    className="carousel-image"
                    key={ photo.photo_id }
                    width={ 240 }
                    src={ photo.url }
                    style={ { overflow: 'hidden' } } />
                ) ) }
              </Carousel>
            }>
            <Meta title={ profile.name } description={ (
              <>
                <div className="text-center">
                  <LikedIcon liked={ profile.liked } />
                </div>
                <br />
                <div className="text-center">
                  <Button
                    className="text-center"
                    type="primary"
                    onClick={ () => console.log( "Liking!!" ) }>
                    Like
                  </Button>
                </div>
              </>
            ) }></Meta>
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