/*
  Warnings:

  - Changed the type of `timestamp` on the `Feature` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.

*/
-- AlterTable
ALTER TABLE "Feature" DROP COLUMN "timestamp",
ADD COLUMN     "timestamp" TIMESTAMP(3) NOT NULL;

-- CreateIndex
CREATE INDEX "Feature_timestamp_idx" ON "Feature"("timestamp");
