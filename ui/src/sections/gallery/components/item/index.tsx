import { Button, Card, Carousel, Col, Image, Space, message } from "antd"
import { Profile } from "../../../../lib/types"
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"

interface Props {
  errorMessage: ( message: string ) => void
  profile: Profile
  refetch: () => void
  searchParams: URLSearchParams
  successMessage: ( message: string ) => void
}
export const GalleryItem = ( {
  errorMessage,
  profile,
  refetch,
  searchParams,
  successMessage
}: Props ) => {

  const { Meta } = Card

  const location = useLocation()
  const navigate = useNavigate()


  const [ deleteLoading, setDeleteLoading ] = useState<boolean>( false )
  const [ likeLoading, setLikeLoading ] = useState<boolean>( false )

  const deleteProfile = async ( profileId: number ) => {
    setDeleteLoading( true )
    const request = await fetch( `/api/users/${ profileId }`, { method: "DELETE" } )
    const response = await request.json()
    if ( request.status === 200 ) {
      successMessage( response.message )
      refetch()
    } else {
      errorMessage( response.message )
    }
    setDeleteLoading( false )
  }

  const likeProfile = async ( profileId: number ) => {
    setLikeLoading( true )
    const request = await fetch( `/api/users/like/${ profileId }`, { method: "POST" } )
    const response = await request.json()
    if ( request.status === 200 ) {
      successMessage( "Profile was liked" )
      refetch()
    } else {
      errorMessage( response.message )
    }
    setLikeLoading( false )
  }

  const LikedIcon = ( { liked }: { liked: boolean } ) => {
    return liked ? (
      <CheckCircleOutlined style={ { fontSize: "24px", color: "green" } } />
    ) : (
      <CloseCircleOutlined style={ { fontSize: "24px", color: "red" } } />
    )
  }

  return (
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
              <Button
                icon={ <LikedIcon liked={ profile.liked } /> }
                onClick={ () => {
                  searchParams.set( "liked", profile.liked ? "1" : "0" )
                  navigate( `${ location.pathname }?${ searchParams.toString() }` )
                } }
                title={ profile.liked === true ? "Liked" : "Not liked" }
                type="text" />
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
  )
}