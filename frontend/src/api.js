import axios from "axios";

export const enhanceImage = async (image) => {
  const formData = new FormData();
  formData.append("file", image);

  const res = await axios.post("http://localhost:8000/enhance", formData, {
    responseType: "blob",
  });

  return URL.createObjectURL(res.data);
};
