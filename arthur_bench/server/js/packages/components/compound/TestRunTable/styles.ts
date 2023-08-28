import primary from "resources/colors/Arthur/primary"
import secondary from "resources/colors/Arthur/secondary"
import { GRAPHIK_LIGHT, MONO_MEDIUM} from "resources/fonts"

const styles = {
    table: {
        borderCollapse: 'collapse',
        border: `1px solid ${primary.ashGrey}`,
        margin: '20px'
    },
    runName: {
        display: 'flex',
        flexDirection: 'column',
        gap: '10px'
    },
    row: {
        height: '60px',
        ':hover': {
            backgroundColor: secondary.lightBlue,
        }

    },
    nameCell: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    empty: {
        backgroundColor: primary.white,
        height: '360px',
        width: '680px',
        border: `1px dashed ${primary.ashGrey}`,
        color: primary.black,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '30px'
    }

}

export const cellStyles = (width?: string) => ({
    width: width ?? 'auto',
    border: `1px solid ${primary.ashGrey}`,
    fontSize: '12px',
    FontFamily: GRAPHIK_LIGHT,
    textAlign: 'left',
    padding: '16px',
})

export const headerCell = (color?: string) => ({
    backgroundColor: color ?? primary.white,
    fontFamily: MONO_MEDIUM,
    border: `1px solid ${primary.ashGrey}`,
    textAlign: 'left',
    fontSize: '16px'
})

export default styles
