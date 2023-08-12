import { Card, Carousel, Col, Image, Row, Tooltip } from "antd"
import { Photo, Profile } from "../../../../lib/types"
import { useState } from "react"
import "./styles.css"
import { Actions } from "../actions"

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
  successMessage
}: Props ) => {

  const { Meta } = Card

  const [ unscheduleLoading, setUnscheduleLoading ] = useState<boolean>( false )
  const [ hideLoading, setHideLoading ] = useState<boolean>( false )
  const [ scheduleLoading, setScheduleLoading ] = useState<boolean>( false )
  const [ unhideLoading, setUnhideLoading ] = useState<boolean>( false )

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

  const scheduleProfile = async ( profileId: number ) => {
    setScheduleLoading( true )
    makeRequest( `/api/users/schedule/${profileId}`, () => {
      setScheduleLoading( false )
    } )
  }

  const unscheduleProfile = async ( profileId: number ) => {
    setUnscheduleLoading( true )
    makeRequest( `/api/users/unschedule/${profileId}`, () => {
      setUnscheduleLoading( false )
    } )
  }

  const hideProfile = async ( profileId: number ) => {
    setHideLoading( true )
    makeRequest( `/api/users/${profileId}/hide`, () => {
      setHideLoading( false )
    } )
  }

  const unhideProfile = async ( profileId: number ) => {
    setUnhideLoading( true )
    makeRequest( `/api/users/${profileId}/restore`, () => {
      setUnhideLoading( false )
    } )
  }

  const ShortBio = ( { bio }: { bio?: string | null } ) => {
    if ( bio === null || bio == undefined ) {
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

  const StatusText = ( { liked, scheduled }: { liked: boolean, scheduled: boolean } ) => {
    if ( liked === true ) {
      return <Col className="text-green" xs={ 16 }><strong>Liked</strong></Col>
    }
    if ( scheduled === true ) {
      return <Col className="text-yellow" xs={ 16 }><strong>Scheduled</strong></Col>
    }
    return <Col className="text-blue" xs={ 16 }><strong>New</strong></Col>
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
            { profile.photos.map( ( photo: Photo ) => (
              <Image
                className="carousel-image"
                key={ photo.photoId }
                width={ 240 }
                src={ photo.url }
                style={ { overflow: 'hidden' } } />
            ) ) }
          </Carousel>
        }>
        <Meta title={ `${profile.name} (${profile.age})` } description={ (
          <>
            <Row className="description-row">
              <Col xs={ 8 }>Status:</Col>
              <StatusText liked={ profile.liked } scheduled={ profile.scheduled } />
            </Row>
            <Row className="description-row">
              <Col xs={ 8 }>Bio:</Col>
              <Col xs={ 16 }>
                <ShortBio bio={ profile?.bio } />
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
                hide={ () => {
                  hideProfile( profile.id )
                } }
                hiding={ hideLoading }
                schedule={ () => {
                  scheduleProfile( profile.id )
                } }
                liked={ profile.liked }
                scheduling={ scheduleLoading }
                scheduled={ profile.scheduled }
                unhide={ () => {
                  unhideProfile( profile.id )
                } }
                unhiding={ unhideLoading }
                unschedule={ () => {
                  unscheduleProfile( profile.id )
                } }
                unscheduling={ unscheduleLoading }
                visible={ profile.visible } />
            </Row>
          </>
        ) }></Meta>
      </Card>
    </Col>
  )
}