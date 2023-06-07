import { DislikeOutlined, LikeOutlined, StopOutlined } from "@ant-design/icons"
import { Button, Col, Tooltip } from "antd"

interface Props {
  hide: () => void
  hiding: boolean
  liked: boolean
  schedule: () => void
  scheduled: boolean
  scheduling: boolean
  unschedule: () => void,
  unscheduling: boolean
}

export const Actions = ( {
  hide,
  hiding,
  liked,
  schedule,
  scheduled,
  scheduling,
  unschedule,
  unscheduling
}: Props ) => {
  return (
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