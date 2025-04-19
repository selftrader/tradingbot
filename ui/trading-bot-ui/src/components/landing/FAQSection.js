import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Container,
  Typography,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const faqs = [
  {
    question: "Is Growth Quantix beginner-friendly?",
    answer:
      "Yes! We provide a plug-and-play system with smart defaults and clear documentation.",
  },
  {
    question: "Can I run my own strategy?",
    answer:
      "No.  as of now we do not support custom strategy.  Our engine supports black box strategy logic and AI-enhanced decisions. We are working on a custom strategy builder for future releases.",
  },
  {
    question: "What brokers are supported?",
    answer:
      "Currently, we support Upstox, Dhan, and Fyers. More integrations are coming soon!",
  },
];

const FAQSection = () => {
  return (
    <Box py={10} sx={{ backgroundColor: "#071d36", color: "#fff" }}>
      <Container maxWidth="md">
        <Typography variant="h4" align="center" fontWeight="bold" mb={4}>
          Frequently Asked Questions
        </Typography>
        {faqs.map((faq, index) => (
          <Accordion
            key={index}
            sx={{ backgroundColor: "#0c1b2a", color: "#fff" }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon sx={{ color: "#3DE1FF" }} />}
            >
              <Typography fontWeight="bold">{faq.question}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography color="gray">{faq.answer}</Typography>
            </AccordionDetails>
          </Accordion>
        ))}
      </Container>
    </Box>
  );
};

export default FAQSection;
