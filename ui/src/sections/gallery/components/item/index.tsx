import { Button, Card, Carousel, Col, Image, Row, Tooltip } from "antd"
import { Profile } from "../../../../lib/types"
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import "./styles.css"

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
    try {
      const request = await fetch( `/api/users/${ profileId }`, { method: "DELETE" } )
      const response = await request.json()
      if ( request.status === 200 ) {
        successMessage( response.message )
        refetch()
      } else {
        errorMessage( response.message )
      }
    } catch ( error: any ) {
      errorMessage( error.message )
    }
    setDeleteLoading( false )
  }

  const likeProfile = async ( profileId: number ) => {
    setLikeLoading( true )
    try {
      const request = await fetch( `/api/users/like/${ profileId }`, { method: "POST" } )
      const response = await request.json()
      if ( request.status === 200 ) {
        successMessage( "Profile was liked" )
        refetch()
      } else {
        errorMessage( response.message )
      }
    } catch ( error: any ) {
      errorMessage( error.message )
    }
    setLikeLoading( false )
  }

  const ShortBio = ( { bio }: { bio: string | null } ) => {
    if ( bio === null ) {
      return <span></span>
    }
    return bio.length < 15 ? (
      <span>{ bio }</span>
    ) : (
      <Tooltip title={ bio }>
        <span>{ bio.substring( 0, 15 ) } ...</span>
      </Tooltip>
    )
  }

  const LikedIcon = ( { liked }: { liked: boolean } ) => {
    return liked ? (
      <CheckCircleOutlined className="liked" />
    ) : (
      <CloseCircleOutlined className="not-liked" />
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
        <Meta title={ `${ profile.name } (${ profile.age })` } description={ (
          <>
            <Row className="description-row">
              <Col className="table" xs={ 8 }>
                <div className="table-cell">Liked:</div>
              </Col>
              <Col xs={ 16 }>
                <Button
                  className="no-pad"
                  icon={ <LikedIcon liked={ profile.liked } /> }
                  onClick={ () => {
                    searchParams.set( "liked", profile.liked ? "1" : "0" )
                    navigate( `${ location.pathname }?${ searchParams.toString() }` )
                  } }
                  title={ profile.liked === true ? "Liked" : "Not liked" }
                  type="text" />
              </Col>
            </Row>
            <Row className="description-row">
              <Col xs={ 8 }>Bio:</Col>
              <Col xs={ 16 }>
                <ShortBio bio={ profile.bio } />
              </Col>
            </Row>
            <Row className="description-row">
              <Col xs={ 8 }>From:</Col>
              <Col xs={ 16 }>{ profile.city }</Col>
            </Row>
            <Row className="description-row">
              <Col xs={ 8 }>Distance:</Col>
              <Col xs={ 16 }>{ profile.distance } km</Col>
            </Row>
            <Row className="description-row actions">
              <Col className="left" xs={ 11 }>
                <Button
                  className="text-center"
                  loading={ likeLoading }
                  onClick={ () => likeProfile( profile.id ) }
                  type="primary">
                  Like
                </Button>
              </Col>
              <Col xs={ 11 } offset={ 1 }>
                <Button
                  className="text-center"
                  danger
                  loading={ deleteLoading }
                  onClick={ () => deleteProfile( profile.id ) }
                  type="primary">
                  Delete
                </Button>
              </Col>
            </Row>
          </>
        ) }></Meta>
      </Card>
    </Col>
  )
}