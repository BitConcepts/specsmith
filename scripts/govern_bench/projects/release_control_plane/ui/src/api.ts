export type Release = {
  id: string;
  service: string;
};

export async function listReleases(): Promise<Release[]> {
  throw new Error("T29: API client not implemented");
}
