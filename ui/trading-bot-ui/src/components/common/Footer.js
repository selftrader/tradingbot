import React from "react";
import {
  Box,
  Container,
  Typography,
  Link,
  Grid,
  IconButton,
  Divider,
  TextField,
  Button,
  Tooltip,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import TwitterIcon from "@mui/icons-material/Twitter";
import FacebookIcon from "@mui/icons-material/Facebook";
import EmailIcon from "@mui/icons-material/Email";

const Footer = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <Box
      component="footer"
      sx={{
        pt: 8,
        pb: 5,
        mt: 8,
        backgroundColor: isDark ? "#0A0B0E" : "#F5F8FA",
        color: isDark ? "#ccc" : "#111",
        borderTop: `2px solid ${theme.palette.primary.main}`,
        backgroundImage: isDark
          ? "radial-gradient(circle at top left, rgba(0,255,255,0.1), transparent)"
          : "none",
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={6} justifyContent="space-between">
          {/* Company Info */}
          <Grid item xs={12} md={4}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              Growth Quantix
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              Revolutionizing trading through Artificial Intelligence. We bring
              automation, insight, and execution to every Indian retail trader.
            </Typography>
          </Grid>

          {/* Quick Links */}
          <Grid item xs={12} md={4}>
            <Typography
              variant="h6"
              fontWeight="bold"
              textAlign="center"
              gutterBottom
            >
              Quick Links
            </Typography>
            <Grid container spacing={1} justifyContent="center">
              {[
                { label: "About Us", href: "/about" },
                { label: "Supported Brokers", href: "#supported-brokers" },
                { label: "Terms & Conditions", href: "/terms" },
                { label: "Privacy Policy", href: "/privacy" },
                { label: "Contact Us", href: "/contact" },
              ].map((link, idx) => (
                <Grid item key={idx}>
                  <Link
                    href={link.href}
                    underline="hover"
                    sx={{
                      color: theme.palette.text.secondary,
                      fontWeight: 500,
                      "&:hover": {
                        color: theme.palette.primary.main,
                      },
                    }}
                  >
                    {link.label}
                  </Link>
                </Grid>
              ))}
            </Grid>
          </Grid>

          {/* Newsletter & Social */}
          <Grid item xs={12} md={4}>
            <Typography
              variant="h6"
              fontWeight="bold"
              textAlign={isMobile ? "center" : "right"}
              gutterBottom
            >
              Stay Connected
            </Typography>

            {/* Newsletter */}
            <Box
              component="form"
              sx={{
                display: "flex",
                gap: 1,
                flexDirection: isMobile ? "column" : "row",
                justifyContent: isMobile ? "center" : "flex-end",
              }}
            >
              <TextField
                variant="outlined"
                size="small"
                placeholder="Your email"
                sx={{
                  backgroundColor: "#fff",
                  borderRadius: "4px",
                  minWidth: "200px",
                }}
              />
              <Button
                variant="contained"
                size="small"
                endIcon={<EmailIcon />}
                sx={{
                  bgcolor: theme.palette.primary.main,
                  color: "#000",
                  fontWeight: "bold",
                  "&:hover": {
                    bgcolor: theme.palette.primary.dark,
                  },
                }}
              >
                Subscribe
              </Button>
            </Box>

            {/* Social Icons */}
            <Box
              mt={2}
              display="flex"
              justifyContent={isMobile ? "center" : "flex-end"}
              gap={1}
            >
              {[
                { icon: <LinkedInIcon />, label: "LinkedIn", link: "#" },
                { icon: <TwitterIcon />, label: "Twitter", link: "#" },
                { icon: <FacebookIcon />, label: "Facebook", link: "#" },
              ].map(({ icon, label, link }, idx) => (
                <Tooltip title={label} arrow key={idx}>
                  <IconButton
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{
                      color: theme.palette.primary.main,
                      transition: "transform 0.2s",
                      "&:hover": {
                        transform: "scale(1.2)",
                        color: theme.palette.primary.light,
                      },
                    }}
                  >
                    {icon}
                  </IconButton>
                </Tooltip>
              ))}
            </Box>
          </Grid>
        </Grid>

        {/* Divider & Copy */}
        <Divider
          sx={{
            my: 4,
            opacity: 0.2,
          }}
        />

        <Typography
          variant="body2"
          textAlign="center"
          sx={{ opacity: 0.6, fontSize: "0.9rem" }}
        >
          &copy; {new Date().getFullYear()} Growth Quantix. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
