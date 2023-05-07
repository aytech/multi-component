import { Card, Carousel, Col, Image, Row, Tooltip } from "antd"
import { Profile } from "../../../../lib/types"
import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import "./styles.css"
import { LikedButton } from "../likedButton"
import { ScheduledButton } from "../scheduledButton"
import { Actions } from "../actions"

interface Props {
  errorMessage: ( message: string ) => void
  profile: Profile
  refetch: () => void
  scheduled: boolean
  searchParams: URLSearchParams
  successMessage: ( message: string ) => void
}
export const GalleryItem = ( {
  errorMessage,
  profile,
  refetch,
  scheduled,
  searchParams,
  successMessage
}: Props ) => {

  const { Meta } = Card

  const location = useLocation()
  const navigate = useNavigate()


  const [ dislikeLoading, setDislikeLoading ] = useState<boolean>( false )
  const [ hideLoading, setHideLoading ] = useState<boolean>( false )
  const [ likeLoading, setLikeLoading ] = useState<boolean>( false )

  const makeRequest = async ( url: string, callback: () => void ) => {
    try {
      const request = await fetch( url, { method: "POST" } )
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
    callback()
  }

  const likeProfile = async ( profileId: number ) => {
    setLikeLoading( true )
    makeRequest( `/api/users/${ profileId }/like`, () => {
      setLikeLoading( false )
    } )
  }

  const dislikeProfile = async ( profileId: number ) => {
    setDislikeLoading( true )
    makeRequest( `/api/users/${ profileId }/dislike`, () => {
      setDislikeLoading( false )
    } )
  }

  const hideProfile = async ( profileId: number ) => {
    setHideLoading( true )
    makeRequest( `/api/users/${ profileId }/hide`, () => {
      setHideLoading( false )
    } )
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
              <Col className="table text-right" xs={ 12 }>
                <ScheduledButton onClick={ () => {
                  searchParams.set( "scheduled", scheduled ? "1" : "0" )
                  navigate( `${ location.pathname }?${ searchParams.toString() }` )
                } } scheduled={ scheduled } />
              </Col>
              <Col xs={ 12 }>
                <LikedButton liked={ profile.liked } onClick={ () => {
                  searchParams.set( "liked", profile.liked ? "1" : "0" )
                  navigate( `${ location.pathname }?${ searchParams.toString() }` )
                } } />
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
              <Actions
                dislike={ () => {
                  dislikeProfile( profile.id )
                } }
                disliking={ dislikeLoading }
                hide={ () => {
                  hideProfile( profile.id )
                } }
                hiding={ hideLoading }
                like={ () => {
                  likeProfile( profile.id )
                } }
                liking={ likeLoading } />
            </Row>
          </>
        ) }></Meta>
      </Card>
    </Col>
  )
}