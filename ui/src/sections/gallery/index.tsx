import { Button, Card, Carousel, Col, Image, Row, Space, message } from "antd"
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import "./styles.css"
import { UsersData } from "../../lib/types"
import { useState } from "react"

interface Props {
  refetch: () => void
  userData: UsersData | null
}

export const Gallery = ( {
  refetch,
  userData
}: Props ) => {

  const { Meta } = Card

  const [ deleteLoading, setDeleteLoading ] = useState<boolean>( false )
  const [ likeLoading, setLikeLoading ] = useState<boolean>( false )

  const [ messageApi ] = message.useMessage();

  const deleteProfile = async ( profileId: number ) => {
    setDeleteLoading( true )
    const response = await fetch( `/api/users/${ profileId }`, { method: "DELETE" } )
    if ( response.status === 200 ) {
      messageApi.success( "Profile was deleted" )
      refetch()
    } else {
      messageApi.error( "Profile was not deleted for some reason" )
    }
  }

  const likeProfile = async ( profileId: number ) => {
    setLikeLoading( true )
    const response = await fetch( `/api/users/like/${ profileId }`, { method: "POST" } )
    if ( response.status === 200 ) {
      messageApi.success( "Profile was liked" )
      refetch()
    } else {
      messageApi.error( "Profile was not liked for some reason" )
    }
  }

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
                  <Space>
                    <Button
                      className="text-center"
                      loading={ likeLoading }
                      onClick={ () => likeProfile( profile.id ) }
                      type="primary">
                      Like
                    </Button>
                    <Button
                      className="text-center"
                      danger
                      loading={ deleteLoading }
                      onClick={ () => deleteProfile( profile.id ) }
                      type="primary">
                      Delete
                    </Button>
                  </Space>
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