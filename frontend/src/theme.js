import { createTheme} from "@mui/material/styles";

// color design
export const tokens = () =>({
    grey: {
        100: "#e0e0e0",
        200: "#c2c2c2",
        300: "#a3a3a3",
        400: "#858585",
        500: "#666666",
        600: "#525252",
        700: "#3d3d3d",
        800: "#292929",
        900: "#141414"
    },
    blue: {
        100: "#d0d1d5",
        200: "#a1a4ab",
        300: "#727681",
        400: "#434957",
        500: "#141b2d",
        600: "#101624",
        700: "#0c101b",
        800: "#080b12",
        900: "#040509"
    },
    green: {
        100: "#dbf5ee",
        200: "#b7ebde",
        300: "#94e2cd",
        400: "#70d8bd",
        500: "#4cceac",
        600: "#3da58a",
        700: "#2e7c67",
        800: "#1e5245",
        900: "#0f2922"
    },
    red: {
        100: "#f8dcdb",
        200: "#f1b9b7",
        300: "#e99592",
        400: "#e2726e",
        500: "#db4f4a",
        600: "#af3f3b",
        700: "#832f2c",
        800: "#58201e",
        900: "#2c100f"
    },
    
});

export const themeSettings = () => {
    const colors = tokens();
    return{
        palette: {
            primary: {
                main: colors.blue[500]
            },
            secondary: {
                main: colors.green[500]
            },
            neutral: {
                dark: colors.blue[700],
                main: colors.blue[500],
                light: colors.blue[100]
            },
            background: {
                default: "#fcfcfc"
            },
        },
        typography: {
            fontFamily: ["Spurce Sans Pro, sans-serif"].join(","),
            fontSize: 12,
            h1: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "40",
            },
            h2: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "32",
            },
            h3: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "24",
            },
            h4: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "20",
            },
            h5: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "16",
            },
            h6: {
                fontFamily: ["Spurce Sans Pro", "sans-serif"].join(","),
                fontSize: "14",
            },
            
        }
    }
}

// function to export theme
export const Theme = createTheme(themeSettings());