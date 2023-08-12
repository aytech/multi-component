import { DislikeOutlined, EyeInvisibleOutlined, LikeOutlined, StopOutlined } from "@ant-design/icons"
import { Button, Col, Tooltip } from "antd"

interface Props {
  hide: () => void
  hiding: boolean
  liked: boolean
  schedule: () => void
  scheduled: boolean
  scheduling: boolean
  unhide: () => void
  unhiding: boolean
  unschedule: () => void
  unscheduling: boolean
  visible: boolean
}

export const Actions = ( {
  hide,
  hiding,
  liked,
  schedule,
  scheduled,
  scheduling,
  unhide,
  unhiding,
  unschedule,
  unscheduling,
  visible
}: Props ) => {
  return visible === false ? (
    <Col className="text-center" xs={ 24 }>
      <Button
        loading={ unhiding }
        onClick={ unhide }
        type="primary">
        <Tooltip title="User is invisible, click to restore">
          <EyeInvisibleOutlined />
        </Tooltip>
      </Button>
    </Col>
  ) : (
    <>
      <Col className="text-center" xs={ unscheduling || hiding ? 6 : scheduling ? 12 : 8 }>
        <Button
          className="btn-green"
          disabled={ scheduled || liked }
          loading={ scheduling }
          onClick={ schedule }
          type="primary">
          <Tooltip title="Like">
            <LikeOutlined />
          </Tooltip>
        </Button>
      </Col>
      <Col className="text-center" xs={ scheduling || hiding ? 6 : unscheduling ? 12 : 8 }>
        <Button
          disabled={ !scheduled }
          loading={ unscheduling }
          onClick={ unschedule }
          type="primary">
          <Tooltip title="Dislike">
            <DislikeOutlined />
          </Tooltip>
        </Button>
      </Col>
      <Col className="text-center" xs={ scheduling || unscheduling ? 6 : hiding ? 12 : 8 }>
        <Button
          danger
          disabled={ liked || scheduled }
          loading={ hiding }
          onClick={ hide }
          type="primary">
          <Tooltip title="Hide">
            <StopOutlined />
          </Tooltip>
        </Button>
      </Col>
    </>
  )
}