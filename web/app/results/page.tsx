import { permanentRedirect } from "next/navigation";

export default function ResultsRedirect() {
  permanentRedirect("/#leaderboard");
}
