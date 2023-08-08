import primary from "resources/colors/Arthur/primary"
import { MONO } from "resources/fonts"

const styles = {
    container: {
        background: primary.white,
        width: '968px',
        minHeight: '575px',
        padding: '32px',
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        fontFamily: MONO,
        filter: 'drop-shadow(0px 2px 12px rgba(26, 0, 22, 0.2))',
        color: primary.black
    },
    header: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    body: {
        display: 'flex',
        justifyContent: 'space-between',
        width: '904px',
        minHeight: '427px',
    },
    column: {
        width: '435px',
    },
    columnHeader: {
        background: primary.mint,
        height: '24px',
        display: 'flex',
        justifyContent: 'center',
        fontSize: '12px',
        alignItems: 'center',
    },
    dataChunk: {
        fontSize: '14px',
        minHeight: '45px',
        padding: '7px',
        display: 'flex',
        flexDirection: 'column',
        overflowWrap: 'anywhere',
        justifyContent: 'space-between',
        margin: '8px 0',
        gap: '8px',
    },
    dataChunkLabel: {
        fontSize: '12px',
    },
    title: {
        fontSize: '24px',
        fontWeight: 400,
        fontStyle: 'normal',
        lineHeight: '38px',
        display: 'flex',
        width: '100%',
    }
}

export default styles
